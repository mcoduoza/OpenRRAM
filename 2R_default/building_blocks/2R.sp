* Include RRAM 
.hdl rram.va

.SUBCKT cell_2r wl_t wl_b bl

* Top RRAM cell and initial condition (HRS)
XR_T wl_tc blc gap_t RRAM I0=1e-4 Vel0=100
.ic V(gap_t)=1.5
.ic V(wl_tc)=0
.ic V(blc)=0

* Bottom RRAM cell and initial condition (LRS)
XR_B blc wl_bc gap_b RRAM I0=1e-4 Vel0=100
.ic V(gap_b)=1.5
.ic V(wl_bc)=0

* Parasitics
* TODO: use PEX numbers instead
Rwl_t wl_t wl_tc 0.25
Cwl_t wl_tc gnd 0.2f
Rwl_b wl_b wl_bc 0.25
Cwl_b wl_bc gnd 0.2f
Rbl bl blc 0.25
Cbl blc gnd 0.2f
.ENDS cell_2r
