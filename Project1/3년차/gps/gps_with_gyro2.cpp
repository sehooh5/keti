#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<unistd.h>
#include<assert.h>
#include<termios.h>
#include<string.h>
#include<sys/time.h>
#include<time.h>
#include<sys/types.h>
#include<errno.h>

static int ret;
static int fd;

#define BAUD 9600 //115200 for JY61 ,9600 for others

int uart_open(int fd,const char *pathname)
{
    fd = open(pathname, O_RDWR|O_NOCTTY);
    if (-1 == fd)
    {
        perror("Can't Open Serial Port");
		return(-1);
	}
    else
		printf("open %s success!\n",pathname);
    if(isatty(STDIN_FILENO)==0)
		printf("standard input is not a terminal device\n");
    else
		printf("isatty success!\n");
    return fd;
}

int uart_set(int fd,int nSpeed, int nBits, char nEvent, int nStop)
{
     struct termios newtio,oldtio;
     if  ( tcgetattr( fd,&oldtio)  !=  0) {
      perror("SetupSerial 1");
	  printf("tcgetattr( fd,&oldtio) -> %d\n",tcgetattr( fd,&oldtio));
      return -1;
     }
     bzero( &newtio, sizeof( newtio ) );
     newtio.c_cflag  |=  CLOCAL | CREAD;
     newtio.c_cflag &= ~CSIZE;
     switch( nBits )
     {
     case 7:
      newtio.c_cflag |= CS7;
      break;
     case 8:
      newtio.c_cflag |= CS8;
      break;
     }
     switch( nEvent )
     {
     case 'o':
     case 'O':
      newtio.c_cflag |= PARENB;
      newtio.c_cflag |= PARODD;
      newtio.c_iflag |= (INPCK | ISTRIP);
      break;
     case 'e':
     case 'E':
      newtio.c_iflag |= (INPCK | ISTRIP);
      newtio.c_cflag |= PARENB;
      newtio.c_cflag &= ~PARODD;
      break;
     case 'n':
     case 'N':
      newtio.c_cflag &= ~PARENB;
      break;
     default:
      break;
     }

     /*设置波特率*/

switch( nSpeed )
     {
     case 2400:
      cfsetispeed(&newtio, B2400);
      cfsetospeed(&newtio, B2400);
      break;
     case 4800:
      cfsetispeed(&newtio, B4800);
      cfsetospeed(&newtio, B4800);
      break;
     case 9600:
      cfsetispeed(&newtio, B9600);
      cfsetospeed(&newtio, B9600);
      break;
     case 115200:
      cfsetispeed(&newtio, B115200);
      cfsetospeed(&newtio, B115200);
      break;
     case 460800:
      cfsetispeed(&newtio, B460800);
      cfsetospeed(&newtio, B460800);
      break;
     default:
      cfsetispeed(&newtio, B9600);
      cfsetospeed(&newtio, B9600);
     break;
     }
     if( nStop == 1 )
      newtio.c_cflag &=  ~CSTOPB;
     else if ( nStop == 2 )
      newtio.c_cflag |=  CSTOPB;
     newtio.c_cc[VTIME]  = 0;
     newtio.c_cc[VMIN] = 0;
     tcflush(fd,TCIFLUSH);

if((tcsetattr(fd,TCSANOW,&newtio))!=0)
     {
      perror("com set error");
      return -1;
     }
     printf("set done!\n");
     return 0;
}

int uart_close(int fd)
{
    assert(fd);
    close(fd);

    return 0;
}
int send_data(int  fd, char *send_buffer,int length)
{
	length=write(fd,send_buffer,length*sizeof(unsigned char));
	return length;
}
int recv_data(int fd, char* recv_buffer,int length)
{
	length=read(fd,recv_buffer,length);
	return length;
}
float a[3],w[3],Angle[3],h[3];

// gps long data 추출
unsigned int get_lognitude(char *chrBuf)
{
	unsigned int lon;
	unsigned int tmp[4];
	int i;

	for(i=0;i<4;i++)
	{
//		printf("**** %x ****", chrBuf[i+2]);

		tmp[i] = (unsigned int)chrBuf[i+2];

//		printf("%d", tmp[i]);
	}

//	printf("\n");

	lon = ((tmp[3] << 24) || (tmp[2] << 16) || (tmp[1] << 8) || tmp[0]) ;


	return lon;
}

// Parsing Data
void ParseData(char chr)
{
		static char chrBuf[100];
		static unsigned char chrCnt=0;
		signed short sData[4];
		unsigned char i;
		char cTemp=0;
		// cmyang
		unsigned int lon;
		unsigned int lat;
		// --

		time_t now;
		chrBuf[chrCnt++]=chr;
		if (chrCnt<11) return;
		for (i=0;i<10;i++) cTemp+=chrBuf[i];
		if ((chrBuf[0]!=0x55)||((chrBuf[1]&0x50)!=0x50)||(cTemp!=chrBuf[10])) {printf("Error:%x %x\r\n",chrBuf[0],chrBuf[1]);memcpy(&chrBuf[0],&chrBuf[1],10);chrCnt--;return;}

		memcpy(&sData[0],&chrBuf[2],8);

		switch(chrBuf[1])
		{
				case 0x51:
				    printf("\r\n[0x51] Acceleration Output start\n");
				    float ax;
				    float ay;
				    float az;

                    signed short tmp[8];

                    for(i=0;i<8;i++)
                    {
                        tmp[i] = (signed short)chrBuf[i+2];
                        printf("\r\ntmp %d ", tmp[i]);
                    }
                    ax = (float) (((tmp[1]<<8)|tmp[0])/32768*16);
                    ay = (float) (((tmp[3]<<8)|tmp[2])/32768*16);
                    az = (float) (((tmp[5]<<8)|tmp[4])/32768*16);
                    printf("\r\nax : %f", ax);
                    printf("\r\nay : %f", ay);
                    printf("\r\naz : %f", az);

// chrBuf 프린트해보기
/*				    for(i=0;i<10;i++)
				    {
				        printf("\r\nchrBuf : ");
				        printf("%c", chrBuf[i]);
				    }
*/
				    printf("\r\n[0x51] Acceleration Output End\n");
				    break;
                case 0x52:
				    break;
				case 0x53:
				    break;
				case 0x54:
				    break;
                case 0x56:
				    break;
				case 0x57:
//					printf(" %x", chrBuf[0]);
//					printf("%x", chrBuf[1]);
//					printf("%x", chrBuf[2]);
//					printf("%x", chrBuf[3]);
//					printf("%x", chrBuf[4]);
//					printf("%x", chrBuf[5]);
//					printf("%x", chrBuf[6]);
//					printf("%x", chrBuf[7]);
//					printf("%x", chrBuf[8]);
//					printf("%x", chrBuf[9]);

					lon = get_lognitude(chrBuf);
//					printf("\n lon : %d, dd: %f, mm : %f\n", lon, (float)(lon/100000000), (float)((lon%10000000)/100000));
					break;
                case 0x58:
				    break;
                case 0x59:
				    break;
                case 0x5A:
				    break;

/*
				case 0x50:
				       printf(" \n********************************** \n");
				       printf("YY : %02d, MM: %02d, %02d, %02d, %02d, %02d, %0d\n", (int)(chrBuf[2]), (int)(chrBuf[3]), (int)(chrBuf[4]), (int)(chrBuf[5]), (int)(chrBuf[6]), (int)(chrBuf[7]), (int)(((unsigned short)(chrBuf[9]<<8))|(unsigned short)chrBuf[8]));
				       printf("********************************** \n");
				       break;

				case 0x51:
					for (i=0;i<3;i++) a[i] = (float)sData[i]/32768.0*16.0;
					time(&now);
					printf("\r\nT:%s a:%6.3f %6.3f %6.3f ",asctime(localtime(&now)),a[0],a[1],a[2]);

					break;
				case 0x52:
					for (i=0;i<3;i++) w[i] = (float)sData[i]/32768.0*2000.0;
					printf("w:%7.3f %7.3f %7.3f ",w[0],w[1],w[2]);
					break;
				case 0x53:
					for (i=0;i<3;i++) Angle[i] = (float)sData[i]/32768.0*180.0;
					printf("A:%7.3f %7.3f %7.3f ",Angle[0],Angle[1],Angle[2]);
					break;
				case 0x54:
					for (i=0;i<3;i++) h[i] = (float)sData[i];
					printf("h:%4.0f %4.0f %4.0f ",h[0],h[1],h[2]);

					break;
*/
		}
		chrCnt=0;
}


// main 동작
int main(void)
{
    char r_buf[1024];
    bzero(r_buf,1024);

    fd = uart_open(fd,"/dev/ttyUSB4");/*串口号/dev/ttySn,USB口号/dev/ttyUSBn */
    if(fd == -1)
    {
        fprintf(stderr,"uart_open error\n");
        exit(EXIT_FAILURE);
    }

    if(uart_set(fd,BAUD,8,'N',1) == -1)
    {
        fprintf(stderr,"uart set failed!\n");
        exit(EXIT_FAILURE);
    }

	FILE *fp;
	fp = fopen("Record.txt","w");
    while(1)
    {
        ret = recv_data(fd,r_buf,44);
        if(ret == -1)
        {
            fprintf(stderr,"uart read failed!\n");
            exit(EXIT_FAILURE);
        }
		for (int i=0;i<ret;i++) {fprintf(fp,"%2X ",r_buf[i]);ParseData(r_buf[i]);}
        usleep(1000);
    }

    ret = uart_close(fd);
    if(ret == -1)
    {
        fprintf(stderr,"uart_close error\n");
        exit(EXIT_FAILURE);
    }

    exit(EXIT_SUCCESS);
}