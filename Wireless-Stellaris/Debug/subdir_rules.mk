################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Each subdirectory must supply rules for building sources it contributes
lmi_fs.obj: ../lmi_fs.c $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: ARM Compiler'
	"C:/ti/ccsv6/tools/compiler/arm_15.12.3.LTS/bin/armcl" -mv7M3 --code_state=16 --abi=eabi -me -O2 -g --include_path="C:/ti/ccsv6/tools/compiler/arm_15.12.3.LTS/include" --include_path="E:/workspace_v6_2/EvalBot_Ethernet" --include_path="E:/StellarisWare" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/src/include" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/src/include/ipv4" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/apps" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/ports/stellaris/include" --include_path="E:/StellarisWare/third_party" --gcc --define=ccs="ccs" --define=PART_LM3S9B92 --define=TARGET_IS_TEMPEST_RB1 --diag_warning=225 --display_error_number --gen_func_subsections=on --ual --preproc_with_compile --preproc_dependency="lmi_fs.d" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '

main.obj: ../main.c $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: ARM Compiler'
	"C:/ti/ccsv6/tools/compiler/arm_15.12.3.LTS/bin/armcl" -mv7M3 --code_state=16 --abi=eabi -me -O2 -g --include_path="C:/ti/ccsv6/tools/compiler/arm_15.12.3.LTS/include" --include_path="E:/workspace_v6_2/EvalBot_Ethernet" --include_path="E:/StellarisWare" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/src/include" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/src/include/ipv4" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/apps" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/ports/stellaris/include" --include_path="E:/StellarisWare/third_party" --gcc --define=ccs="ccs" --define=PART_LM3S9B92 --define=TARGET_IS_TEMPEST_RB1 --diag_warning=225 --display_error_number --gen_func_subsections=on --ual --preproc_with_compile --preproc_dependency="main.d" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '

startup_ccs.obj: ../startup_ccs.c $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: ARM Compiler'
	"C:/ti/ccsv6/tools/compiler/arm_15.12.3.LTS/bin/armcl" -mv7M3 --code_state=16 --abi=eabi -me -O2 -g --include_path="C:/ti/ccsv6/tools/compiler/arm_15.12.3.LTS/include" --include_path="E:/workspace_v6_2/EvalBot_Ethernet" --include_path="E:/StellarisWare" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/src/include" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/src/include/ipv4" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/apps" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/ports/stellaris/include" --include_path="E:/StellarisWare/third_party" --gcc --define=ccs="ccs" --define=PART_LM3S9B92 --define=TARGET_IS_TEMPEST_RB1 --diag_warning=225 --display_error_number --gen_func_subsections=on --ual --preproc_with_compile --preproc_dependency="startup_ccs.d" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '


