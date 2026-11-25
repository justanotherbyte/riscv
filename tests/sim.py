from pathlib import Path
from xml.etree import ElementTree

import pytest
from cocotb_tools.runner import get_runner

SRC = Path(__file__).resolve().parent.parent / "src"


def run(toplevel: str, sources: list[str], test_module: str, testcase: str | None = None) -> None:
    """Build `sources` (relative to src/) with Verilator and run the cocotb tests in `test_module`.

    With `testcase`, run only that test in a fresh simulator so no state leaks in from other tests.
    """
    runner = get_runner("verilator")
    build_dir = Path(__file__).parent.parent / "sim_build" / toplevel
    runner.build(
        sources=[SRC / s for s in sources],
        hdl_toplevel=toplevel,
        build_dir=build_dir,
        always=False,  # rebuild only when sources change, so per-test runs reuse one build
        waves=True,
        build_args=["-Wno-PINMISSING",],
    )
    test_dir = build_dir / testcase if testcase else build_dir  # sim cwd: dump.vcd and results land here
    results = test_dir / "results.xml"
    try:
        runner.test(
            hdl_toplevel=toplevel,
            test_module=test_module,
            testcase=testcase,
            test_dir=test_dir,
            build_dir=build_dir,
            waves=True,
            results_xml=str(results),
        )
    except SystemExit:
        # The runner exits with only a code; pull each failing test's traceback out of its results file instead.
        if not results.is_file():
            raise
        failures = [
            f"{case.get('name')}:\n{problem.text or problem.get('message')}"
            for case in ElementTree.parse(results).iter("testcase")
            for problem in [*case.iter("failure"), *case.iter("error")]
        ]
        if not failures:
            raise
    else:
        return
    pytest.fail("\n\n".join(failures), pytrace=False)  # outside `except` so pytest doesn't print the SystemExit chain
