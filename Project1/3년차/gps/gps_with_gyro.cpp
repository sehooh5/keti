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
float a[9],w[9],Angle[9],h[9],ph[9],gps[9],s[9],q[9],sp[9];
void ParseData(char chr)
{
		static char chrBuf[100];
		static unsigned char chrCnt=0;
		signed short sData[4];
		unsigned char i;
		char cTemp=0;
		time_t now;
		chrBuf[chrCnt++]=chr;
		if (chrCnt<11) return;
		for (i=0;i<10;i++) cTemp+=chrBuf[i];
		if ((chrBuf[0]!=0x55)||((chrBuf[1]&0x50)!=0x50)||(cTemp!=chrBuf[10])) {printf("Error:%x %x\r\n",chrBuf[0],chrBuf[1]);memcpy(&chrBuf[0],&chrBuf[1],10);chrCnt--;return;}

		memcpy(&sData[0],&chrBuf[2],8);

		switch(chrBuf[1])
		{
				case 0x51:
					for (i=0;i<6;i++) a[i] = (float)sData[i]/32768.0*16.0;
					for (i=6;i<8;i++) a[i] = (float)sData[i]/100;
					time(&now);
					printf("\r\nT:%s a:%6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f"
					,asctime(localtime(&now)),a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7]);
					break;
				case 0x52:
					for (i=0;i<6;i++) w[i] = (float)sData[i]/32768.0*2000.0;
					for (i=6;i<8;i++) w[i] = (float)sData[i]/100;
					printf("\n w:%7.3f %7.3f %7.3f %7.3f %7.3f %7.3f %7.3f %7.3f"
					,w[0],w[1],w[2],w[3],w[4],w[5],w[6],w[7]);
					break;
				case 0x53:
					for (i=0;i<6;i++) Angle[i] = (float)sData[i]/32768.0*180.0;
					for (i=6;i<8;i++) Angle[i] = (float)sData[i];
					printf("\n A:%7.3f %7.3f %7.3f %7.3f %7.3f %7.3f %7.3f %7.3f"
					,Angle[0],Angle[1],Angle[2],Angle[3],Angle[4],Angle[5],Angle[6],Angle[7]);
					break;
				case 0x54:
					for (i=0;i<8;i++) h[i] = (float)sData[i];
					printf("\n h:%4.0f %4.0f %4.0f %4.0f %4.0f %4.0f %4.0f %4.0f"
					,h[0],h[1],h[2],h[3],h[4],h[5],h[6],h[7]);
				case 0x56:
					for (i=0;i<8;i++) ph[i] = (float)sData[i];
					printf("\n ph:%f %f %f %f %f %f %f %f"
					,ph[0],ph[1],ph[2],ph[3],ph[4],ph[5],ph[6],ph[7]);
				case 0x57:
					for (i=0;i<8;i++) gps[i] = (float)sData[i];
					printf("\n gps:%f %f %f %f %f %f %f %f",gps[0],gps[1],gps[2],gps[3],gps[4],gps[5],gps[6],gps[7]);
					break;
				case 0x58:
					for (i=0;i<8;i++) s[i] = (float)sData[i];
					printf("\n s:%f %f %f %f %f %f %f %f",s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7]);
					break;
				case 0x59:
					for (i=0;i<8;i++) q[i] = (float)sData[i];
					printf("\n q:%f %f %f %f %f %f %f %f",q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7]);
					break;
				case 0x5A:
					for (i=0;i<8;i++) sp[i] = (float)sData[i];
					printf("\n sp:%f %f %f %f %f %f %f %f",sp[0],sp[1],sp[2],sp[3],sp[4],sp[5],sp[6],sp[7]);
					break;
		}
		chrCnt=0;
}

int main(void)
{
    char r_buf[1024];
    bzero(r_buf,1024);

    fd = uart_open(fd,"/dev/ttyUSB2");/*串口号/dev/ttySn,USB口号/dev/ttyUSBn */
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
        ret = recv_data(fd,r_buf,110);
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
