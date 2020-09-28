
char dataString[50] = {0};
int ohm =0 ;
int pwmpin = 3;
int auxconvert =0;
int convert =0;
int convert2 =0;
float vout = 0;
int i = 0;
void setup(){
  
Serial.begin(9600);
pinMode(pwmpin,OUTPUT);  

}

void loop(){

//Descobre resistencia atraves de um resistor de 1k
float reading;
float media = 0; 
reading = analogRead(A0);

reading = (1023 / reading)  - 1;     // (1023/ADC - 1) 
reading = 1000 / reading;  // 10K / (1023/ADC - 1)

//Tira media das ultimas 5 leituras a cada 3 segundos 
for (i = 0; i < 5; i++) {
  reading = analogRead(A0);
  reading = (1023 / reading)  - 1;     // (1023/ADC - 1) 
  reading = 1000 / reading;  // 10K / (1023/ADC - 1)
  
  media = media + reading;
  //Serial.println(reading);
  delay(3000);
}
float R2 = media/5; 
int convert =0;
//Convert em PWM para saida em tensao e envia os dados para o raspberry via porta serial
if(i > 4){
    float vout = (convert*5.0)/255.0;
    if(R2 > 0)
    {      
      convert =2.9474*R2-20.034 ;
      vout = ((convert*5.0)/255.0)+2.0;

      if (convert < 0) {convert = 0;}
      if (convert > 255) {convert = 255;}
      analogWrite(pwmpin,convert); 
      //Serial.print("Vout: ");
      //Serial.print(vout);
      //Serial.print("  - R2: ");
      //Serial.print(R2);
      //Serial.print("  - Convert: ");
      //Serial.println(convert);
      ohm = (int)R2;
      sprintf(dataString,"%02X",ohm); // convert a value to hexa 
      Serial.println(dataString);   // send the data
     }      
  }
  //analogWrite(pwmpin2,255);
  i++;
}
