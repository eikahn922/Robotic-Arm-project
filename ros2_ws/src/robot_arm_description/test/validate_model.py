#!/usr/bin/env python3
"""Static validation for the robot_arm_description URDF/Xacro model.

Runs with the Python standard library only - no ROS, no numpy - so it works on
the development Mac as well as inside the Ubuntu VM. It checks the real project
files rather than re-stating constants: every geometric assertion is recomputed
from the committed Xacro and the committed STL meshes.

    python3 test/validate_model.py

Exits 0 if every check passes, 1 otherwise.
"""
from __future__ import annotations

import math
import os
import re
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XACRO = os.path.join(PKG, "urdf", "robot_arm.urdf.xacro")

REQUIRED_JOINTS = {
    "base_yaw_joint": "revolute",
    "shoulder_joint": "revolute",
    "elbow_joint": "revolute",
    "wrist_joint": "revolute",
    "gripper_joint": "revolute",
    "gripper_base_joint": "fixed",
    "right_gripper_joint": "revolute",
}
CONTROLS = ["base_yaw_joint", "shoulder_joint", "elbow_joint", "wrist_joint", "gripper_joint"]
DUPLICATED = {
    "STL/gripper_gear.stl": 2,
    "STL/gripper_connecting_link.stl": 2,
    "STL/gripper_finger.stl": 2,
}
ROOT = "base_link"

_failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> bool:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}{('  - ' + detail) if detail else ''}")
    if not ok:
        _failures.append(label)
    return ok


def section(title: str) -> None:
    print(f"\n{title}\n{'-' * len(title)}")


# ---------------------------------------------------------------- matrix maths
def rpy_to_R(r, p, y):
    cr, sr, cp, sp, cy, sy = math.cos(r), math.sin(r), math.cos(p), math.sin(p), math.cos(y), math.sin(y)
    return [
        [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
        [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
        [-sp, cp * sr, cp * cr],
    ]


def make_T(xyz, rpy):
    R = rpy_to_R(*rpy)
    return [R[i] + [xyz[i]] for i in range(3)] + [[0.0, 0.0, 0.0, 1.0]]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def apply_T(T, v):
    return [sum(T[i][j] * v[j] for j in range(3)) + T[i][3] for i in range(3)]


def axis_rotation(axis, theta):
    n = math.sqrt(sum(c * c for c in axis)) or 1.0
    x, y, z = (c / n for c in axis)
    c, s, t = math.cos(theta), math.sin(theta), 1 - math.cos(theta)
    R = [
        [t * x * x + c, t * x * y - s * z, t * x * z + s * y],
        [t * x * y + s * z, t * y * y + c, t * y * z - s * x],
        [t * x * z - s * y, t * y * z + s * x, t * z * z + c],
    ]
    return [R[i] + [0.0] for i in range(3)] + [[0.0, 0.0, 0.0, 1.0]]


def _eigvals_sym3(M):
    """Closed-form eigenvalues of a symmetric 3x3 matrix (no numpy)."""
    p1 = M[0][1] ** 2 + M[0][2] ** 2 + M[1][2] ** 2
    q = (M[0][0] + M[1][1] + M[2][2]) / 3.0
    if p1 == 0:
        return [M[0][0], M[1][1], M[2][2]]
    p2 = sum((M[i][i] - q) ** 2 for i in range(3)) + 2 * p1
    p = math.sqrt(p2 / 6.0)
    B = [[(M[i][j] - (q if i == j else 0)) / p for j in range(3)] for i in range(3)]
    detB = (B[0][0] * (B[1][1] * B[2][2] - B[1][2] * B[2][1])
            - B[0][1] * (B[1][0] * B[2][2] - B[1][2] * B[2][0])
            + B[0][2] * (B[1][0] * B[2][1] - B[1][1] * B[2][0]))
    phi = math.acos(max(-1.0, min(1.0, detB / 2.0))) / 3.0
    e1 = q + 2 * p * math.cos(phi)
    e3 = q + 2 * p * math.cos(phi + 2 * math.pi / 3)
    return [e1, 3 * q - e1 - e3, e3]


# ------------------------------------------------------------------- STL reader
def stl_vertices(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) < 84:
        return None, 0, False
    tris = struct.unpack("<I", data[80:84])[0]
    consistent = len(data) == 84 + 50 * tris
    verts = []
    if consistent:
        for i in range(tris):
            off = 84 + i * 50 + 12
            for j in range(3):
                verts.append(struct.unpack("<3f", data[off + j * 12: off + j * 12 + 12]))
    return verts, tris, consistent


# ----------------------------------------------------------------- parse xacro
_SAFE = re.compile(r"^[0-9eE+\-*/(). ]+$")


def _eval_expr(expr: str, props: dict) -> str:
    """Evaluate one ${...} body: substitute properties, then do the arithmetic.

    Only bare numbers and the four operators survive the safety check, so this
    cannot execute arbitrary code from the Xacro.
    """
    body = expr
    for _ in range(5):
        before = body
        for key, value in props.items():
            body = re.sub(r"\b" + re.escape(key) + r"\b", "(" + value + ")", body)
        if body == before:
            break
    if not _SAFE.match(body):
        raise ValueError(f"unsafe or unresolved xacro expression: {expr!r} -> {body!r}")
    return repr(eval(body, {"__builtins__": {}}, {}))       # noqa: S307 - guarded above


def load_model():
    raw = open(XACRO).read()
    props = dict(re.findall(r'<xacro:property\s+name="([^"]+)"\s+value="([^"]+)"', raw))
    text = re.sub(r"\$\{([^}]*)\}", lambda m: _eval_expr(m.group(1), props), raw)
    return raw, text, props


def origin_of(el):
    o = el.find("origin")
    if o is None:
        return make_T([0, 0, 0], [0, 0, 0])
    return make_T([float(v) for v in o.get("xyz", "0 0 0").split()],
                  [float(v) for v in o.get("rpy", "0 0 0").split()])


def main() -> int:
    print("=" * 72)
    print("robot_arm_description - static model validation")
    print("=" * 72)
    print(f"package: {PKG}")

    # ---------------------------------------------------------- 1. xacro/XML
    section("1. Xacro expansion and XML structure")
    if not check("xacro file exists", os.path.exists(XACRO), XACRO):
        return 1
    raw, text, props = load_model()
    leftover = re.findall(r"\$\{[^}]+\}", text)
    check("all xacro properties expand", not leftover, ", ".join(leftover))
    check("properties declared", bool(props), ", ".join(f"{k}={v}" for k, v in props.items()))
    try:
        root = ET.fromstring(text)
        check("expanded XML parses", True)
    except ET.ParseError as exc:
        check("expanded XML parses", False, str(exc))
        return 1

    links = {l.get("name"): l for l in root.findall("link")}
    joints = []
    for j in root.findall("joint"):
        mimic = j.find("mimic")
        limit = j.find("limit")
        joints.append({
            "name": j.get("name"), "type": j.get("type"),
            "parent": j.find("parent").get("link") if j.find("parent") is not None else None,
            "child": j.find("child").get("link") if j.find("child") is not None else None,
            "T": origin_of(j),
            "axis": [float(v) for v in j.find("axis").get("xyz").split()] if j.find("axis") is not None else None,
            "mimic": (mimic.get("joint"), float(mimic.get("multiplier", 1)), float(mimic.get("offset", 0))) if mimic is not None else None,
            "limit": (float(limit.get("lower")), float(limit.get("upper"))) if limit is not None and limit.get("lower") else None,
        })
    check("links and joints found", bool(links) and bool(joints), f"{len(links)} links, {len(joints)} joints")

    # ----------------------------------------------------- 2. tree structure
    section("2. Tree structure")
    names = [j["name"] for j in joints]
    check("joint names unique", len(names) == len(set(names)))
    check("link names unique", len(links) == len(root.findall("link")))
    dangling = [f"{j['name']}:{n}" for j in joints for n in (j["parent"], j["child"]) if n not in links]
    check("every joint parent/child link exists", not dangling, ", ".join(dangling))

    children = [j["child"] for j in joints]
    check("no link has two parent joints", len(children) == len(set(children)))
    roots = [n for n in links if n not in children]
    check("exactly one root link", len(roots) == 1, f"roots={roots}")
    check(f"root is {ROOT}", roots == [ROOT], f"roots={roots}")

    # cycle / reachability check by walking from the root
    adj = {}
    for j in joints:
        adj.setdefault(j["parent"], []).append(j["child"])
    seen, stack, cyclic = set(), list(roots), False
    while stack:
        node = stack.pop()
        if node in seen:
            cyclic = True
            break
        seen.add(node)
        stack.extend(adj.get(node, []))
    check("no cycles", not cyclic)
    check("all links reachable from root", seen == set(links),
          f"unreachable={sorted(set(links) - seen)}")

    # --------------------------------------------------- 3. required joints
    section("3. Required joints and controls")
    by_name = {j["name"]: j for j in joints}
    for name, jtype in REQUIRED_JOINTS.items():
        j = by_name.get(name)
        check(f"{name} exists and is {jtype}", j is not None and j["type"] == jtype,
              "missing" if j is None else f"type={j['type']}")
    controls = [j["name"] for j in joints
                if j["type"] in ("revolute", "prismatic") and not j["mimic"]]
    check("exactly five user controls", controls == CONTROLS, f"got {controls}")

    # ------------------------------------------------------------ 4. mimic
    section("4. Mimic joint")
    mimics = [j for j in joints if j["mimic"]]
    check("exactly one mimic joint", len(mimics) == 1, f"got {[m['name'] for m in mimics]}")
    for m in mimics:
        target, mult, off = m["mimic"]
        check(f"{m['name']} mimic target exists", target in by_name, f"target={target}")
        check(f"{m['name']} mimic target is a control", target in CONTROLS, f"target={target}")
        check(f"{m['name']} multiplier is non-zero and finite",
              math.isfinite(mult) and mult != 0, f"multiplier={mult} offset={off}")
        tgt = by_name.get(target)
        if tgt and tgt["limit"] and m["limit"]:
            lo, hi = tgt["limit"]
            reach = sorted((lo * mult + off, hi * mult + off))
            check(f"{m['name']} limits cover the mimicked range",
                  m["limit"][0] <= reach[0] + 1e-9 and m["limit"][1] >= reach[1] - 1e-9,
                  f"needs {reach}, has {list(m['limit'])}")

    # ------------------------------------------------------------ 5. limits
    section("5. Joint limits")
    for j in joints:
        if j["type"] == "fixed":
            continue
        if not check(f"{j['name']} declares a limit", j["limit"] is not None):
            continue
        lo, hi = j["limit"]
        check(f"{j['name']} limits finite and ordered",
              math.isfinite(lo) and math.isfinite(hi) and lo < hi, f"[{lo}, {hi}]")
        check(f"{j['name']} zero is inside its range", lo <= 0.0 <= hi, f"[{lo}, {hi}]")
        check(f"{j['name']} has a rotation axis",
              j["axis"] is not None and any(abs(c) > 1e-12 for c in j["axis"]), f"axis={j['axis']}")

    # ------------------------------------------------------------- 6. meshes
    section("6. Mesh references")
    counts = {}
    for name, link in links.items():
        for vis in link.findall("visual"):
            mesh = vis.find("geometry/mesh")
            if mesh is None:
                continue
            rel = mesh.get("filename").replace("package://robot_arm_description/", "")
            counts[rel] = counts.get(rel, 0) + 1
            path = os.path.join(PKG, rel)
            if check(f"{rel} resolves", os.path.exists(path)):
                _, tris, consistent = stl_vertices(path)
                check(f"{rel} is a valid binary STL", consistent, f"{tris} triangles")
    for rel, want in DUPLICATED.items():
        check(f"{rel} referenced exactly {want}x", counts.get(rel, 0) == want, f"got {counts.get(rel, 0)}")

    # ------------------------------------------- 7. gripper geometry, from CAD
    section("7. Gripper kinematics recomputed from the committed meshes")
    finger = os.path.join(PKG, "STL", "gripper_finger.stl")
    left = by_name.get("gripper_joint")
    right = by_name.get("right_gripper_joint")
    if os.path.exists(finger) and left and right and right["mimic"]:
        verts, _, ok_stl = stl_vertices(finger)
        vis = {}
        for side, link_name in (("L", left["child"]), ("R", right["child"])):
            for v in links[link_name].findall("visual"):
                mesh = v.find("geometry/mesh")
                if mesh is not None and mesh.get("filename").endswith("gripper_finger.stl"):
                    vis[side] = origin_of(v)
        if ok_stl and len(vis) == 2:
            def tip(T_vis):
                best, far = None, -1.0
                for v in verts:
                    p = apply_T(T_vis, [c * 0.001 for c in v])
                    d = sum(c * c for c in p)
                    if d > far:
                        far, best = d, p
                return best

            tips = {s: tip(vis[s]) for s in vis}
            mult = right["mimic"][1]

            def separation(theta):
                pL = apply_T(matmul(left["T"], axis_rotation(left["axis"], theta)), tips["L"])
                pR = apply_T(matmul(right["T"], axis_rotation(right["axis"], theta * mult)), tips["R"])
                return math.dist(pL, pR)

            closed = separation(0.0)
            hi = left["limit"][1] if left["limit"] else 0.3
            opened = separation(hi)
            check("gripper is closed at joint zero (STEP neutral pose)", closed < 0.005,
                  f"{closed * 1000:.2f} mm between fingertips")
            check("positive rotation opens the jaws", opened > closed,
                  f"{closed * 1000:.2f} mm -> {opened * 1000:.2f} mm at {hi} rad")
            samples = [separation(hi * i / 12.0) for i in range(2, 13)]
            check("opening is monotonic over the commanded range",
                  all(b > a for a, b in zip(samples, samples[1:])),
                  f"max opening {max(samples) * 1000:.1f} mm")
        else:
            check("gripper finger visuals located on both sides", False, f"found {sorted(vis)}")

    # ------------------------------------------------ 7b. collision geometry
    section("7b. Collision geometry")
    # Meshing gears and a gripper that is closed at neutral mean the two finger
    # boxes necessarily overlap. Self-collision between the sides must be
    # disabled downstream (Gazebo self_collide / MoveIt SRDF), so it is expected
    # here rather than treated as a defect.
    EXPECTED_OVERLAP = {frozenset(("left_gripper_link", "right_gripper_link"))}
    prim_links = {}
    for name, link in links.items():
        prims = []
        for col in link.findall("collision"):
            geom = col.find("geometry")
            kind = None
            for tag in ("box", "cylinder", "sphere", "mesh"):
                if geom.find(tag) is not None:
                    kind = tag
                    break
            prims.append((kind, geom, origin_of(col)))
        prim_links[name] = prims
        check(f"{name} has collision geometry", bool(prims), f"{len(prims)} primitive(s)")
        for kind, _, _ in prims:
            check(f"{name} collision uses a primitive, not a mesh", kind != "mesh", f"kind={kind}")

    # Every collision primitive must contain the visual geometry it is meant to
    # cover. The gripper sides intentionally cover only the finger, so coverage
    # is asserted per mesh rather than per link.
    UNCOVERED = {("left_gripper_link", "STL/gripper_gear.stl"),
                 ("left_gripper_link", "STL/gripper_connecting_link.stl"),
                 ("right_gripper_link", "STL/gripper_gear.stl"),
                 ("right_gripper_link", "STL/gripper_connecting_link.stl")}

    def inside(prims, p):
        for kind, geom, Tc in prims:
            R = [[Tc[i][j] for j in range(3)] for i in range(3)]
            d = [p[i] - Tc[i][3] for i in range(3)]
            loc = [sum(R[k][i] * d[k] for k in range(3)) for i in range(3)]
            if kind == "box":
                s = [float(x) / 2 for x in geom.find("box").get("size").split()]
                if all(abs(loc[i]) <= s[i] + 1e-6 for i in range(3)):
                    return True
            elif kind == "cylinder":
                cyl = geom.find("cylinder")
                rad, length = float(cyl.get("radius")), float(cyl.get("length"))
                if math.hypot(loc[0], loc[1]) <= rad + 1e-6 and abs(loc[2]) <= length / 2 + 1e-6:
                    return True
        return False

    for name, link in links.items():
        prims = prim_links.get(name) or []
        if not prims:
            continue
        for vis in link.findall("visual"):
            mesh = vis.find("geometry/mesh")
            if mesh is None:
                continue
            rel = mesh.get("filename").replace("package://robot_arm_description/", "")
            scale = float((mesh.get("scale") or "1 1 1").split()[0])
            vv, _, ok_stl = stl_vertices(os.path.join(PKG, rel))
            if not ok_stl:
                continue
            Tv = origin_of(vis)
            step = max(1, len(vv) // 400)
            pts = [apply_T(Tv, [c * scale for c in vv[i]]) for i in range(0, len(vv), step)]
            frac = sum(1 for p in pts if inside(prims, p)) / len(pts)
            short = rel.split("/")[-1]
            if (name, rel) in UNCOVERED:
                check(f"{name}/{short} is intentionally uncovered (internal mechanism)",
                      frac < 0.5, f"{frac * 100:.1f}% covered")
            else:
                check(f"{name}/{short} fully inside its collision primitive", frac >= 0.999,
                      f"{frac * 100:.1f}% of {len(pts)} sampled vertices")

    # ------------------------------------------------ 7c. inertial properties
    section("7c. Inertial properties")
    for name, link in links.items():
        inert = link.find("inertial")
        if not check(f"{name} has an inertial block", inert is not None):
            continue
        mass = float(inert.find("mass").get("value"))
        check(f"{name} mass is positive and finite", math.isfinite(mass) and mass > 0,
              f"{mass * 1000:.2f} g")
        el = inert.find("inertia")
        ixx, iyy, izz = (float(el.get(k)) for k in ("ixx", "iyy", "izz"))
        ixy, ixz, iyz = (float(el.get(k)) for k in ("ixy", "ixz", "iyz"))
        M = [[ixx, ixy, ixz], [ixy, iyy, iyz], [ixz, iyz, izz]]
        check(f"{name} inertia entries finite",
              all(math.isfinite(v) for row in M for v in row))
        # Sylvester's criterion: all leading principal minors positive
        d1 = ixx
        d2 = ixx * iyy - ixy * ixy
        d3 = (ixx * (iyy * izz - iyz * iyz)
              - ixy * (ixy * izz - iyz * ixz)
              + ixz * (ixy * iyz - iyy * ixz))
        check(f"{name} inertia tensor is positive-definite", d1 > 0 and d2 > 0 and d3 > 0,
              f"minors {d1:.3e}, {d2:.3e}, {d3:.3e}")
        # principal moments must satisfy the triangle inequality for a real body
        p = sorted(_eigvals_sym3(M))
        check(f"{name} principal moments satisfy the triangle inequality",
              p[0] + p[1] >= p[2] * (1 - 1e-9),
              f"{p[0]:.3e} + {p[1]:.3e} >= {p[2]:.3e}")

    # ------------------------------------------------- 8. repository hygiene
    section("8. Repository hygiene")
    try:
        tracked = subprocess.run(["git", "ls-files"], cwd=PKG, capture_output=True, text=True,
                                 check=True).stdout.split()
        junk = [f for f in tracked
                if re.search(r"(^|/)(build|install|log)/|\.DS_Store$|__pycache__|\.pyc$", f)]
        check("no build artifacts or .DS_Store tracked", not junk, ", ".join(junk[:5]))
    except Exception as exc:                                    # not a git checkout
        print(f"  [SKIP] git hygiene check - {exc}")

    # ---------------------------------------------------------------- result
    print("\n" + "=" * 72)
    if _failures:
        print(f"FAILED - {len(_failures)} check(s):")
        for f in _failures:
            print(f"  - {f}")
        return 1
    print("ALL CHECKS PASSED")
    print("=" * 72)
    print("\nStatic validation only. RViz, check_urdf, and any ROS runtime behaviour")
    print("must still be verified in the Ubuntu VM - see docs/VM_HANDOFF.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
