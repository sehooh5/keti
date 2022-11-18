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

//0x51 Acceleration data 추출
float get_acceleration(char *chrBuf, int num)
{
    float ax; float ay; float az; float t;
    signed short tmp[8];
    unsigned char i;

    for(i=0;i<8;i++){
        tmp[i] = (signed short)chrBuf[i+2];
    }

    if (num==1){
        ax = ((float)((tmp[1]<<8)|tmp[0]))/32768*16;
        return ax;
    }
    else if (num==2){
        ay = ((float)((tmp[3]<<8)|tmp[2]))/32768*16;
        return ay;
    }
    else if (num==3){
        az = ((float)((tmp[5]<<8)|tmp[4]))/32768*16;
        return az;
    }
    else if (num==4){
        t = ((float)((tmp[7]<<8)|tmp[6]))/100;
        return t;
    }
    else{
        return 999.999999;
    }
}
//0x52 Angular Velocity data 추출
float get_angular(char *chrBuf, int num)
{
    float wx; float wy; float wz; float t;
    signed short tmp[8];
    unsigned char i;

    for(i=0;i<8;i++){
        tmp[i] = (signed short)chrBuf[i+2];
    }

    if (num==1){
        wx = ((float)((tmp[1]<<8)|tmp[0]))/32768*2000;
        return wx;
    }
    else if (num==2){
        wy = ((float)((tmp[3]<<8)|tmp[2]))/32768*2000;
        return wy;
    }
    else if (num==3){
        wz = ((float)((tmp[5]<<8)|tmp[4]))/32768*2000;
        return wz;
    }
    else if (num==4){
        t = ((float)((tmp[7]<<8)|tmp[6]))/100;
        return t;
    }
    else{
        return 999.999999;
    }
}
//0x53 Angle data 추출
float get_angle(char *chrBuf, int num)
{
    float roll; float pitch; float yaw; float t;
    signed short tmp[8];
    unsigned char i;

    for(i=0;i<8;i++){
        tmp[i] = (signed short)chrBuf[i+2];
    }

    if (num==1){
        roll = ((float)((tmp[1]<<8)|tmp[0]))/32768*180;
        return roll;
    }
    else if (num==2){
        pitch = ((float)((tmp[3]<<8)|tmp[2]))/32768*180;
        return pitch;
    }
    else if (num==3){
        yaw = ((float)((tmp[5]<<8)|tmp[4]))/32768*180;
        return yaw;
    }
    else if (num==4){
        t = ((float)((tmp[7]<<8)|tmp[6]))/100;
        return t;
    }
    else{
        return 999.999999;
    }
}
//0x54 Magnetic data 추출
float get_magnetic(char *chrBuf, int num)
{
    float mx; float my; float mz; float t;
    signed short tmp[8];
    unsigned char i;

    for(i=0;i<8;i++){
        tmp[i] = (signed short)chrBuf[i+2];
    }

    if (num==1){
        mx = ((float)((tmp[1]<<8)|tmp[0]));
        return mx;
    }
    else if (num==2){
        my = ((float)((tmp[3]<<8)|tmp[2]));
        return my;
    }
    else if (num==3){
        mz = ((float)((tmp[5]<<8)|tmp[4]));
        return mz;
    }
    else if (num==4){
        t = ((float)((tmp[7]<<8)|tmp[6]))/100;
        return t;
    }
    else{
        return 999.999999;
    }
}
//0x56 Atmospheric data 추출
float get_atmospheric(char *chrBuf, int num)
{
    float press; float h;
    signed int tmp[8];// int로 변경
    unsigned char i;

    for(i=0;i<8;i++){
        tmp[i] = (signed int)chrBuf[i+2];// int로 변경
    }

    if (num==1){
        press = (float)((tmp[3]<<24)|(tmp[2]<<16)|(tmp[1]<<8)|tmp[0]);
        return press;
    }
    else if (num==2){
        h = ((float)((tmp[7]<<24)|(tmp[6]<<16)|(tmp[5]<<8)|tmp[4]))/100;
        return h;
    }
    else{
        return 999.999999;
    }
}
//0x57 GPS data 추출
float get_gpsData(char *chrBuf, int num)
{
    float lon; float lat;
    signed int tmp[8];// int로 변경
    unsigned char i;

    for(i=0;i<8;i++){
        tmp[i] = (signed int)chrBuf[i+2];// int로 변경
    }

    if (num==1){
        lon = (float)((tmp[3]<<24)|(tmp[2]<<16)|(tmp[1]<<8)|tmp[0]);
        return lon;
    }
    else if (num==2){
        lat = ((float)((tmp[7]<<24)|(tmp[6]<<16)|(tmp[5]<<8)|tmp[4]));
        return lat;
    }
    else{
        return 999.999999;
    }
}
//0x58 Ground Speed data 추출
float get_groundSpeed(char *chrBuf, int num)
{
    float gh; float gy; float gv;
    signed short tmp[8];
    unsigned char i;

    for(i=0;i<8;i++){
        tmp[i] = (signed short)chrBuf[i+2];
    }

    if (num==1){
        gh = ((float)((tmp[1]<<8)|tmp[0]))/10;
        return gh;
    }
    else if (num==2){
        gy = ((float)((tmp[3]<<8)|tmp[2]))/10;
        return gy;
    }
    else if (num==3){
        gv = ((float)((tmp[7]<<24)|(tmp[6]<<16)|(tmp[5]<<8)|tmp[4]))/1000;
        return gv;
    }
    else{
        return 999.999999;
    }
}

// 변수 설정
float ax; float ay; float az; float t; //0x51
float wx; float wy; float wz; //0x52
float roll; float pitch; float yaw;//0x53
float mx; float my; float mz;//0x54
float press; float h; //0x56
float lon; float lat; float lon_dd; float lat_dd; float lon_mm; float lat_mm;//0x57
float gh; float gy; float gv;//0x58

// Parsing Data
void ParseData(char chr)
{
		static char chrBuf[100];
		static unsigned char chrCnt=0;
		unsigned char i;
		char cTemp=0;
		time_t now;
		chrBuf[chrCnt++]=chr;
		if (chrCnt<11) return;
		for (i=0;i<10;i++) cTemp+=chrBuf[i];
		if ((chrBuf[0]!=0x55)||((chrBuf[1]&0x50)!=0x50)||(cTemp!=chrBuf[10])) {printf("Error:%x %x\r\n",chrBuf[0],chrBuf[1]);memcpy(&chrBuf[0],&chrBuf[1],10);chrCnt--;return;}


		switch(chrBuf[1])
		{
				case 0x51:
//				    printf("\r\n[0x51] Acceleration Output");
                    ax = get_acceleration(chrBuf, 1);
                    ay = get_acceleration(chrBuf, 2);
                    az = get_acceleration(chrBuf, 3);
                    t = get_acceleration(chrBuf, 4);
                    printf("[0x51] ax : %f ay : %f az : %f t : %f\r\n", ax, ay, az, t);
				    break;
                case 0x52:
//				    printf("\r\n[0x52] Angular Velocity Output");
                    wx = get_angular(chrBuf,1);
                    wy = get_angular(chrBuf,2);
                    wz = get_angular(chrBuf,3);
                    t = get_angular(chrBuf,4);
                    printf("[0x52] wx : %f wy : %f wz : %f t : %f\r\n", wx, wy, wz, t);
				    break;
				case 0x53:
                    roll = get_angle(chrBuf,1);
                    pitch = get_angle(chrBuf,2);
                    yaw = get_angle(chrBuf,3);
                    t = get_angle(chrBuf,4);
                    printf("[0x53] roll : %f pitch : %f yaw : %f t : %f\r\n", roll, pitch, yaw, t);
				    break;
				case 0x54:
                    mx = get_magnetic(chrBuf,1);
                    my = get_magnetic(chrBuf,2);
                    mz = get_magnetic(chrBuf,3);
                    t = get_magnetic(chrBuf,4);
                    printf("[0x54] mx : %f my : %f mz : %f t : %f\r\n", mx, my, mz, t);
				    break;
                case 0x56:
                    press = get_atmospheric(chrBuf,1);
                    h = get_atmospheric(chrBuf,2);
                    printf("[0x56] press : %f h : %f\r\n", press, h);
				    break;
				case 0x57:
                    lon = get_gpsData(chrBuf,1);
                    lat = get_gpsData(chrBuf,2);

                    lon_dd = lon/100000000;
//                    lon_mm = (((double)lon)%100000000)/100000;
                    lat_dd = lat/100000000;
//                    lat_mm = (((double)lat)%100000000)/100000;
                    printf("[0x57] lon : %f lat : %f\r\n",lon_dd,lat_dd);
//                    printf("[0x57] lon : %f.%f lat : %f.%f\r\n",lon_dd,lon_mm,lat_dd,lat_mm);
				    break;
                case 0x58:
                    gh = get_groundSpeed(chrBuf,1);
                    gy = get_groundSpeed(chrBuf,2);
                    gv = get_groundSpeed(chrBuf,3);
                    printf("[0x58] gh : %f gy : %f gv : %f\r\n", gh, gy, gv);
				    break;
                case 0x59:
				    break;
                case 0x5A:
				    break;

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
        usleep(100);
    }

    ret = uart_close(fd);
    if(ret == -1)
    {
        fprintf(stderr,"uart_close error\n");
        exit(EXIT_FAILURE);
    }

    exit(EXIT_SUCCESS);
}