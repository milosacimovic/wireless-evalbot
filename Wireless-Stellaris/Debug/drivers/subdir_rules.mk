################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Each subdirectory must supply rules for building sources it contributes
drivers/io.obj: ../drivers/io.c $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: ARM Compiler'
	"C:/ti/ccsv6/tools/compiler/arm_15.12.3.LTS/bin/armcl" -mv7M3 --code_state=16 --abi=eabi -me -O2 -g --include_path="C:/ti/ccsv6/tools/compiler/arm_15.12.3.LTS/include" --include_path="E:/workspace_v6_2/EvalBot_Ethernet" --include_path="E:/StellarisWare" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/src/include" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/src/include/ipv4" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/apps" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/ports/stellaris/include" --include_path="E:/StellarisWare/third_party" --gcc --define=ccs="ccs" --define=PART_LM3S9B92 --define=TARGET_IS_TEMPEST_RB1 --diag_warning=225 --display_error_number --gen_func_subsections=on --ual --preproc_with_compile --preproc_dependency="drivers/io.d" --obj_directory="drivers" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '

drivers/motor.obj: ../drivers/motor.c $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: ARM Compiler'
	"C:/ti/ccsv6/tools/compiler/arm_15.12.3.LTS/bin/armcl" -mv7M3 --code_state=16 --abi=eabi -me -O2 -g --include_path="C:/ti/ccsv6/tools/compiler/arm_15.12.3.LTS/include" --include_path="E:/workspace_v6_2/EvalBot_Ethernet" --include_path="E:/StellarisWare" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/src/include" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/src/include/ipv4" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/apps" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/ports/stellaris/include" --include_path="E:/StellarisWare/third_party" --gcc --define=ccs="ccs" --define=PART_LM3S9B92 --define=TARGET_IS_TEMPEST_RB1 --diag_warning=225 --display_error_number --gen_func_subsections=on --ual --preproc_with_compile --preproc_dependency="drivers/motor.d" --obj_directory="drivers" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '

drivers/sensors.obj: ../drivers/sensors.c $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: ARM Compiler'
	"C:/ti/ccsv6/tools/compiler/arm_15.12.3.LTS/bin/armcl" -mv7M3 --code_state=16 --abi=eabi -me -O2 -g --include_path="C:/ti/ccsv6/tools/compiler/arm_15.12.3.LTS/include" --include_path="E:/workspace_v6_2/EvalBot_Ethernet" --include_path="E:/StellarisWare" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/src/include" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/src/include/ipv4" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/apps" --include_path="E:/StellarisWare/third_party/lwip-1.3.2/ports/stellaris/include" --include_path="E:/StellarisWare/third_party" --gcc --define=ccs="ccs" --define=PART_LM3S9B92 --define=TARGET_IS_TEMPEST_RB1 --diag_warning=225 --display_error_number --gen_func_subsections=on --ual --preproc_with_compile --preproc_dependency="drivers/sensors.d" --obj_directory="drivers" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '


