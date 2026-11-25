import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from sim import run


@cocotb.test
async def test_pc_dff(dut):
    instruction = 0xFFC4A303 # lw x6 -4(x9)
    cocotb.start_soon(
      Clock(dut.clk, 10, unit="ns").start()
    )

    dut.pc_next.value = instruction

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.pc.value == instruction


def test_pc():
    run("program_counter", ["pc.sv"], "test_pc")
