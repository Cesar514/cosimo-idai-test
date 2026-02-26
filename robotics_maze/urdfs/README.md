# URDF Assets (Optional External Sources)

This folder can host extra robot assets beyond `pybullet_data`. External assets
are optional: keep simulation defaults pointed at `pybullet_data` whenever
`robotics_maze/urdfs/external` is missing or empty.

## Fetch Scripts (macOS-friendly)

From repository root:

```bash
# Fetch all configured sources
./robotics_maze/scripts/fetch_urdfs.sh

# List sources
./robotics_maze/scripts/fetch_urdfs.sh --list

# Fetch only one source
./robotics_maze/scripts/fetch_urdfs.sh turtlebot3

# Force refresh existing downloads
./robotics_maze/scripts/fetch_urdfs.sh --force
```

The script uses `git` sparse checkout when available and falls back to GitHub
archive download if needed, so it works on standard macOS setups.

## Expected Layout

```text
robotics_maze/
  urdfs/
    README.md
    external/
      turtlebot3/
        SOURCE.json
        LICENSE
        README.md
        turtlebot3_description/
          urdf/
          meshes/
      husky/
        SOURCE.json
        LICENSE
        README.md
        husky_description/
          urdf/
          meshes/
```

## Included Sources and Caveats

1. `turtlebot3`
License: Apache-2.0 (verify upstream `LICENSE` in downloaded folder).
Usage caveat: URDFs are mostly directly usable; still validate mesh URI
resolution in your local loader.

2. `husky`
License: BSD-3-Clause-style terms (verify upstream `LICENSE`).
Usage caveat: the full Husky model flow is xacro-centric in ROS; for direct
PyBullet use you may need a pre-expanded plain URDF.

## Runtime Default Behavior

Do not require these downloads for normal execution. If external folders are
absent, runner code should continue loading built-in models from
`pybullet_data.getDataPath()`.
