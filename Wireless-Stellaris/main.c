#include "inc/hw_ints.h"
#include "inc/hw_memmap.h"
#include "inc/hw_nvic.h"
#include "inc/hw_types.h"
#include "driverlib/ethernet.h"
#include "driverlib/flash.h"
#include "driverlib/gpio.h"
#include "driverlib/interrupt.h"
#include "driverlib/pin_map.h"
#include "driverlib/rom.h"
#include "driverlib/sysctl.h"
#include "driverlib/systick.h"
#include "utils/locator.h"
#include "utils/lwiplib.h"
#include "utils/uartstdio.h"
#include "drivers/io.h"
#include "drivers/sensors.h"
#include "drivers/motor.h"

//
// Defines for setting up the system clock.
//
//*****************************************************************************
#define SYSTICKHZ               100
#define SYSTICKMS               (1000 / SYSTICKHZ)

//
// Defines the maximum motor speed
//
//*****************************************************************************
#define MAX_SPEED 100

//*****************************************************************************
//
// The most recently assigned IP address.  This is used to detect when the IP
// address has changed (due to DHCP/AutoIP) so that the new address can be
// printed.
//
//*****************************************************************************
static unsigned long g_ulLastIPAddr = 0;

//*****************************************************************************
//
// The error routine that is called if the driver library encounters an error.
//
//*****************************************************************************
#ifdef DEBUG
void
__error__(char *pcFilename, unsigned long ulLine)
{
}
#endif

//*****************************************************************************
//
// Required by lwIP library to support any host-related timer functions.
//
//*****************************************************************************
void lwIPHostTimerHandler(void) {
	unsigned long ulIPAddress;

	//
	// Get the local IP address.
	//
	ulIPAddress = lwIPLocalIPAddrGet();

	//
	// Check if IP address has changed.
	//
	if (ulIPAddress != g_ulLastIPAddr) {
		g_ulLastIPAddr = ulIPAddress;
	}
}
//
// Needed for toggling LEDs when going reverse
//
int reverse = 0;
int led = 1;
int counter = 0;

// speed variable
int speed = MAX_SPEED / 2;

//*****************************************************************************
//
// The interrupt handler for the SysTick interrupt.
//
//*****************************************************************************
void SysTickIntHandler(void) {
	//
	// Call the lwIP timer handler.
	//
	lwIPTimer(SYSTICKMS);

	// if going reverse toggle LEDs
	if (reverse == 1) {
		counter++;
		if ((counter % 40) == 0) {
			if(led == 1){
				LED_Toggle(LED_1);
			}else if(led == 2){
				LED_Toggle(LED_2);
			}
			if((counter % 80) == 0){
				if(led == 1)
					led = 2;
				else if(led ==2)
					led = 1;
			}
		}
	}
}

//
// Incoming data buffer
//
char dataBuffer[1024];

//
// Close the TCP/IP connection
//
static void close_conn(struct tcp_pcb *pcb) {
	tcp_arg(pcb, NULL);
	tcp_sent(pcb, NULL);
	tcp_recv(pcb, NULL);
	tcp_close(pcb);
}

//
// The function that handles movement depending on incoming characters
//
static void movementHandler(char command, struct tcp_pcb *pcb) {
	// go forward
	if (dataBuffer[0] == 'w' || dataBuffer[0] == 'W') {
		reverse = 0;
		counter = 0;
		LED_On(LED_1);
		LED_On(LED_2);
		MotorDir(RIGHT_SIDE, FORWARD);
		MotorDir(LEFT_SIDE, FORWARD);
		MotorRun(RIGHT_SIDE);
		MotorRun(LEFT_SIDE);
		UARTprintf("FORWARD");
	}

	// turn left
	if (dataBuffer[0] == 'a') {
		LED_Off(LED_1);
		LED_On(LED_2);
		MotorDir(RIGHT_SIDE, FORWARD);
		MotorRun(RIGHT_SIDE);
		MotorStop(LEFT_SIDE);
		UARTprintf("TURN L");
	}

	// rotate left
	if (dataBuffer[0] == 'A') {
		reverse = 0;
		counter = 0;
		LED_Off(LED_1);
		LED_On(LED_2);
		MotorDir(RIGHT_SIDE, FORWARD);
		MotorDir(LEFT_SIDE, REVERSE);
		MotorRun(RIGHT_SIDE);
		MotorRun(LEFT_SIDE);
		UARTprintf("ROTATE L");
	}

	// go backward
	if (dataBuffer[0] == 's' || dataBuffer[0] == 'S') {
		reverse = 1;
		LED_On(LED_1);
		led = 1;
		LED_Off(LED_2);
		MotorDir(RIGHT_SIDE, REVERSE);
		MotorDir(LEFT_SIDE, REVERSE);
		MotorRun(RIGHT_SIDE);
		MotorRun(LEFT_SIDE);
		UARTprintf("BACKWARD");
	}

	// turn right
	if (dataBuffer[0] == 'd') {
		LED_On(LED_1);
		LED_Off(LED_2);
		MotorDir(LEFT_SIDE, FORWARD);
		MotorStop(RIGHT_SIDE);
		MotorRun(LEFT_SIDE);
		UARTprintf("TURN R");
	}

	// rotate right
	if (dataBuffer[0] == 'D') {
		reverse = 0;
		counter = 0;
		LED_On(LED_1);
		LED_Off(LED_2);
		MotorDir(LEFT_SIDE, FORWARD);
		MotorDir(RIGHT_SIDE, REVERSE);
		MotorRun(RIGHT_SIDE);
		MotorRun(LEFT_SIDE);
		UARTprintf("ROTATE R");
	}

	// stop motors
	if (dataBuffer[0] == 'X' || dataBuffer[0] == 'x') {
		reverse = 0;
		counter = 0;
		LED_Off(LED_1);
		LED_Off(LED_2);
		MotorStop(RIGHT_SIDE);
		MotorStop(LEFT_SIDE);
		UARTprintf("STOP");
	}

	// increase speed
	if (dataBuffer[0] == '+') {
		if (speed < (MAX_SPEED - 10)) {
			speed += 5;
			MotorSpeed(LEFT_SIDE, speed << 8);
			MotorSpeed(RIGHT_SIDE, speed << 8);
		}
		UARTprintf("FASTER");
	}

	// decrease speed
	if (dataBuffer[0] == '-') {
		if (speed > 0) {
			speed -= 5;
			MotorSpeed(LEFT_SIDE, speed << 8);
			MotorSpeed(RIGHT_SIDE, speed << 8);
		}
		UARTprintf("SLOWER");
	}

	// close connection
	if (dataBuffer[0] == 'C' || dataBuffer[0] == 'c') {
		close_conn(pcb);
		LED_Off(LED_1);
		LED_Off(LED_2);
		MotorStop(RIGHT_SIDE);
		MotorStop(LEFT_SIDE);
		UARTprintf("CLOSE");
	}

}

static err_t echo_recv(void *arg, struct tcp_pcb *pcb, struct pbuf *p,
		err_t err) {
	int i;
	int len;
	char *pc;

	if (err == ERR_OK && p != NULL) {
		/* Inform TCP that we have taken the data. */
		tcp_recved(pcb, p->tot_len);

		// pointer to the pay load
		pc = (char *) p->payload;

		// size of the pay load
		len = p->tot_len;

		//copy to our own buffer
		for (i = 0; i < len; i++)
			dataBuffer[i] = pc[i];

		// handle the incoming data
		movementHandler(dataBuffer[0], pcb);

		// Free the packet buffer
		pbuf_free(p);

		// check output buffer capacity
		if (len > tcp_sndbuf(pcb))
			len = tcp_sndbuf(pcb);
		// Send out the data
		err = tcp_write(pcb, dataBuffer, len, 0);
		tcp_sent(pcb, NULL);
	} else {
		pbuf_free(p);
	}

	if (err == ERR_OK && p == NULL) {
		close_conn(pcb);
	}
	return ERR_OK;
}

static err_t echo_accept(void *arg, struct tcp_pcb *pcb, err_t err) {
	LWIP_UNUSED_ARG(arg);
	LWIP_UNUSED_ARG(err);
	tcp_setprio(pcb, TCP_PRIO_MIN);
	tcp_recv(pcb, echo_recv);
	tcp_err(pcb, NULL);
	tcp_poll(pcb, NULL, 4);
	return ERR_OK;
}

int main(void) {
	unsigned long ulUser0, ulUser1;
	unsigned char pucMACArray[8];

	//
	// Initialization
	//
	LEDsInit();
	MotorsInit();
	MotorSpeed(LEFT_SIDE, speed << 8);
	MotorSpeed(RIGHT_SIDE, speed << 8);
	MotorDir(LEFT_SIDE, FORWARD);
	MotorDir(RIGHT_SIDE, FORWARD);

	//
	// Set the clocking to run directly from the crystal.
	//
	ROM_SysCtlClockSet(SYSCTL_SYSDIV_1 | SYSCTL_USE_OSC | SYSCTL_OSC_MAIN |
	SYSCTL_XTAL_16MHZ);

	//
	// Initialize the UART.
	//
	ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
	GPIOPinConfigure(GPIO_PA0_U0RX);
	GPIOPinConfigure(GPIO_PA1_U0TX);
	ROM_GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);
	UARTStdioInit(0);
	UARTprintf("\033[2JEthernet with lwIP\n");

	//
	// Enable and Reset the Ethernet Controller.
	//
	ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_ETH);
	ROM_SysCtlPeripheralReset(SYSCTL_PERIPH_ETH);

	//
	// Enable Port F for Ethernet LEDs.
	//
	ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
	GPIOPinConfigure(GPIO_PF2_LED1);
	GPIOPinConfigure(GPIO_PF3_LED0);
	GPIOPinTypeEthernetLED(GPIO_PORTF_BASE, GPIO_PIN_2 | GPIO_PIN_3);

	//
	// Configure SysTick for a periodic interrupt.
	//
	ROM_SysTickPeriodSet(ROM_SysCtlClockGet() / SYSTICKHZ);
	ROM_SysTickEnable();
	ROM_SysTickIntEnable();

	//
	// Enable processor interrupts.
	//
	ROM_IntMasterEnable();

	//
	// Read the MAC address from the user registers.
	//
	ROM_FlashUserGet(&ulUser0, &ulUser1);

	//
	// Convert the 24/24 split MAC address from NV ram into a 32/16 split MAC
	// address needed to program the hardware registers, then program the MAC
	// address into the Ethernet Controller registers.
	//
	pucMACArray[0] = ((ulUser0 >> 0) & 0xff);
	pucMACArray[1] = ((ulUser0 >> 8) & 0xff);
	pucMACArray[2] = ((ulUser0 >> 16) & 0xff);
	pucMACArray[3] = ((ulUser1 >> 0) & 0xff);
	pucMACArray[4] = ((ulUser1 >> 8) & 0xff);
	pucMACArray[5] = ((ulUser1 >> 16) & 0xff);

	//
	// Initialze the lwIP library, using DHCP.
	//
	lwIPInit(pucMACArray, 0, 0, 0, IPADDR_USE_DHCP);

	//
	// Setup the device locator service.
	//
	LocatorInit();
	LocatorMACAddrSet(pucMACArray);
	LocatorAppTitleSet("EvalBot Ethernet Controller");

	//
	// Open a new TCP connection, bind to port 23
	//
	struct tcp_pcb *ptel_pcb;
	ptel_pcb = tcp_new();
	tcp_bind(ptel_pcb, IP_ADDR_ANY, 23);

	//
	// Infinite loop, listen for new connections
	//
	while (1) {
		ptel_pcb = tcp_listen(ptel_pcb);
		tcp_accept(ptel_pcb, echo_accept);
	}
}
