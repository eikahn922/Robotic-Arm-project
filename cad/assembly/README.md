# Final Robot Arm Assembly

[`Robot-Arm-Final-Assembly.SLDASM`](Robot-Arm-Final-Assembly.SLDASM) is the final native SolidWorks assembly. Its component models are organized by subsystem in the parent [`cad/`](../) directory.

## Verify Component References

SolidWorks assembly documents reference external part and subassembly files. Before distributing the assembly as a portable release:

1. Open the original assembly in SolidWorks.
2. Select **File > Find References** and enable **Include broken references**. Any entry marked **File not found** identifies a missing component.
3. Select **File > Pack and Go** and save all related files into one folder or ZIP archive.

The repository uses descriptive filenames and subsystem folders, which may differ from paths saved inside the original assembly. A Pack and Go package is the safest way to preserve every dependency for another SolidWorks user.

See the official SolidWorks documentation for [Find References](https://help.solidworks.com/2024/English/solidworks/sldworks/HIDD_FINDREFERENCES_HELP.htm) and [Pack and Go](https://help.solidworks.com/2025/english/SolidWorks/Sldworks/r_pack_go_db.htm).
