#!/usr/bin/env bash

set -u
set -o pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_FILE="${ROOT_DIR}/robotics_maze/testing/TEST_RUN_LOG.md"
SCREENSHOT_DIR="${ROOT_DIR}/robotics_maze/testing/screenshots"

declare -a STEP_LABELS=()
declare -a STEP_CODES=()
declare -a STEP_NOTES=()
declare -a CREATED_SCREENSHOTS=()

OVERALL_STATUS=0

infer_probable_cause() {
  local output_file="$1"

  if grep -qi "No module named .*mujoco" "$output_file"; then
    echo "MuJoCo Python dependency appears to be missing."
    return
  fi
  if grep -qi "No module named .*pybullet" "$output_file"; then
    echo "PyBullet dependency appears to be missing."
    return
  fi
  if grep -qi "No module named" "$output_file"; then
    echo "One or more Python dependencies are not installed in the current environment."
    return
  fi
  if grep -qi "float() argument must be a string or a number, not 'tuple'" "$output_file"; then
    echo "Planner output path format is incompatible with simulator waypoint parsing (nested tuples where numeric coordinates are expected)."
    return
  fi
  if grep -qi "permission denied" "$output_file"; then
    echo "Filesystem permission issue while executing a command or writing outputs."
    return
  fi
  if grep -qi "command not found" "$output_file"; then
    echo "Required command is unavailable in the current shell environment."
    return
  fi
  if grep -qi "Traceback (most recent call last)" "$output_file"; then
    echo "Python runtime error; see traceback in command output."
    return
  fi
  echo "See command output for details."
}

record_step_result() {
  local label="$1"
  local code="$2"
  local note="$3"
  STEP_LABELS+=("$label")
  STEP_CODES+=("$code")
  STEP_NOTES+=("$note")
}

run_and_log() {
  local label="$1"
  shift

  local output_file
  output_file="$(mktemp)"
  local status=0
  local cause=""

  {
    echo "## ${label}"
    echo
    echo "**Command**"
    echo '```bash'
    printf '%q ' "$@"
    echo
    echo '```'
    echo
    echo "**Output**"
    echo '```text'
  } >> "${LOG_FILE}"

  if "$@" >"${output_file}" 2>&1; then
    status=0
  else
    status=$?
  fi

  cat "${output_file}" >> "${LOG_FILE}"
  echo >> "${LOG_FILE}"
  echo '```' >> "${LOG_FILE}"
  echo >> "${LOG_FILE}"
  echo "**Exit status:** ${status}" >> "${LOG_FILE}"

  if [ "${status}" -ne 0 ]; then
    cause="$(infer_probable_cause "${output_file}")"
    echo >> "${LOG_FILE}"
    echo "**Probable cause:** ${cause}" >> "${LOG_FILE}"
    OVERALL_STATUS=1
    record_step_result "${label}" "${status}" "FAIL: ${cause}"
  else
    record_step_result "${label}" "${status}" "PASS"
  fi

  echo >> "${LOG_FILE}"
  rm -f "${output_file}"
  return 0
}

record_skipped() {
  local label="$1"
  local reason="$2"

  {
    echo "## ${label}"
    echo
    echo "**Command**"
    echo '```text'
    echo "SKIPPED"
    echo '```'
    echo
    echo "**Output**"
    echo '```text'
    echo "${reason}"
    echo '```'
    echo
    echo "**Exit status:** SKIPPED"
    echo
  } >> "${LOG_FILE}"

  record_step_result "${label}" "SKIPPED" "SKIPPED: ${reason}"
}

collect_generated_screenshots() {
  local label="$1"
  local source_dir="$2"

  local status=0
  local found=0
  local cause=""
  local src_file=""

  {
    echo "## ${label}"
    echo
    echo "**Command**"
    echo '```bash'
    echo "find ${source_dir} -maxdepth 1 -type f -name '*.png' | sort"
    echo '```'
    echo
    echo "**Output**"
    echo '```text'
  } >> "${LOG_FILE}"

  if [ ! -d "${source_dir}" ]; then
    echo "source directory missing: ${source_dir}" >> "${LOG_FILE}"
    status=1
    cause="Expected screenshot output directory was not created."
  else
    while IFS= read -r src_file; do
      [ -z "${src_file}" ] && continue
      echo "${src_file}" >> "${LOG_FILE}"
      CREATED_SCREENSHOTS+=("${src_file}")
      found=$((found + 1))
    done < <(find "${source_dir}" -maxdepth 1 -type f -name "*.png" | sort)

    if [ "${found}" -eq 0 ]; then
      echo "no PNG files found in ${source_dir}" >> "${LOG_FILE}"
      status=1
      cause="Screenshot automation command completed but produced no PNG files."
    fi
  fi

  echo '```' >> "${LOG_FILE}"
  echo >> "${LOG_FILE}"
  echo "**Exit status:** ${status}" >> "${LOG_FILE}"

  if [ "${status}" -ne 0 ]; then
    echo >> "${LOG_FILE}"
    echo "**Probable cause:** ${cause}" >> "${LOG_FILE}"
    OVERALL_STATUS=1
    record_step_result "${label}" "${status}" "FAIL: ${cause}"
  else
    record_step_result "${label}" "${status}" "PASS: found ${found} file(s)"
  fi

  echo >> "${LOG_FILE}"
  return 0
}

write_summary() {
  local i=0
  local rendered_status=""

  {
    echo "## Summary"
    echo
    echo "| Step | Status | Notes |"
    echo "|---|---|---|"
  } >> "${LOG_FILE}"

  for i in "${!STEP_LABELS[@]}"; do
    rendered_status="${STEP_CODES[$i]}"
    if [ "${rendered_status}" = "0" ]; then
      rendered_status="PASS"
    elif [ "${rendered_status}" = "SKIPPED" ]; then
      rendered_status="SKIPPED"
    else
      rendered_status="FAIL (${rendered_status})"
    fi
    printf '| %s | %s | %s |\n' \
      "${STEP_LABELS[$i]}" \
      "${rendered_status}" \
      "${STEP_NOTES[$i]}" >> "${LOG_FILE}"
  done

  echo >> "${LOG_FILE}"
  if [ "${#CREATED_SCREENSHOTS[@]}" -gt 0 ]; then
    echo "### Produced Screenshots" >> "${LOG_FILE}"
    echo >> "${LOG_FILE}"
    for src_file in "${CREATED_SCREENSHOTS[@]}"; do
      echo "- ${src_file}" >> "${LOG_FILE}"
    done
    echo >> "${LOG_FILE}"
  else
    echo "### Produced Screenshots" >> "${LOG_FILE}"
    echo >> "${LOG_FILE}"
    echo "- none" >> "${LOG_FILE}"
    echo >> "${LOG_FILE}"
  fi

  if [ "${OVERALL_STATUS}" -eq 0 ]; then
    echo "**Overall status:** PASS" >> "${LOG_FILE}"
  else
    echo "**Overall status:** FAIL" >> "${LOG_FILE}"
  fi
}

main() {
  export PYTHONHASHSEED=0
  mkdir -p "${SCREENSHOT_DIR}"
  rm -f "${SCREENSHOT_DIR}"/*.png

  {
    echo "# Robotics Maze Simulation Test Run Log"
    echo
    echo "- Date (UTC): $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "- Working directory: ${ROOT_DIR}"
    echo "- PYTHONHASHSEED: ${PYTHONHASHSEED}"
    echo
  } > "${LOG_FILE}"

  cd "${ROOT_DIR}" || exit 1

  run_and_log \
    "Deterministic run: astar" \
    python3 robotics_maze/src/main.py --planner astar --episodes 3 --maze-size 11 --seed 42

  run_and_log \
    "Deterministic run: weighted_astar" \
    python3 robotics_maze/src/main.py --planner weighted_astar --episodes 3 --maze-size 11 --seed 42

  run_and_log \
    "Deterministic run: fringe_search" \
    python3 robotics_maze/src/main.py --planner fringe_search --episodes 3 --maze-size 11 --seed 42

  if [ -f "${ROOT_DIR}/robotics_maze/scripts/capture_regression_screenshots.py" ]; then
    run_and_log \
      "Capture regression screenshots" \
      python3 robotics_maze/scripts/capture_regression_screenshots.py --output-dir "${SCREENSHOT_DIR}" --require-mujoco
    collect_generated_screenshots \
      "Collect regression screenshots" \
      "${SCREENSHOT_DIR}"
  else
    record_skipped \
      "Capture regression screenshots" \
      "Script not found: robotics_maze/scripts/capture_regression_screenshots.py"
  fi

  write_summary
  return "${OVERALL_STATUS}"
}

main "$@"
