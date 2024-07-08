 #include <Stepper.h>



 const int steps_per_revolution = 2048;

  int location = 0;
  String command;
  String x="";
  int rotationcw=0;
  int rotationccw=0;

 Stepper stepper1(steps_per_revolution,2,4,3,5);
 Stepper stepper2(steps_per_revolution,6,8,7,9);
 Stepper stepper3(steps_per_revolution,10,12,11,13);
 Stepper stepper4(steps_per_revolution,A5,A3,A4,A2);
 //ir and led
  #define ir_left A0
#define ir_right A1

// // buzzers


 void setup() {
//   // put your setup code here, to run once:


    Serial.begin(9600);
    
   while(!Serial);
    pinMode(ir_left,INPUT);
    
//   //pin of stepper

   stepper1.setSpeed(10);
   stepper2.setSpeed(10);
   stepper3.setSpeed(10);
   stepper4.setSpeed(10);
   // ir
    
}

 
 void loop() {

   char y;
   if(Serial.available()>0)
   {

     y =  Serial.read();
     
     Serial.println(y);

     if(y=='1')
     {
             
          move_left();
          
     }
     else if(y == '0')
     {
 
        move_Tocenter();
     }
     else if(y == '2')
     {
      
        move_right();
     }
  }
 }


void move_right()
{
 //digitalWrite(buz_right,HIGH);
 if (location<=0){
     Serial.println("moving right");   

  for(int i = 0 ;i<=9;i++)
  {     
    ir_right_read();
  
    stepper1.step(200);//2048
    delay(200);
    ir_right_read();

    stepper2.step(-200);
    delay(200);
    
    ir_right_read();
    stepper3.step(200);
    delay(200);
    ir_right_read();
    stepper4.step(-200);
    delay(200);
      
    }       
  
  location++;
  if (location==1)
    Serial.println("barrier at the right");
  else if(location==0)
    Serial.println("barrier at the center");
  }
  
}


void move_left()
{
 Serial.println("moving left");   

 if(location>=0){
  for(int i = 0 ;i<=9;i++)
  { 
    ir_left_read();
    stepper1.step(-200);
    delay(200);
    ir_left_read();
    stepper2.step(200);
    delay(200);
    ir_left_read();
    stepper3.step(-200);
    delay(200);
    ir_left_read();
    stepper4.step(200);
    delay(200);

  }       
  
  location--;
  if (location==-1)
    Serial.println("finished and barrier now at the left");
  else if(location==0)
    Serial.println("finished and barrier now at the center");
 }
}


void move_Tocenter()
{
  if (location==1)
  {
  move_left();
  location = 0;
  }
  else if (location== -1)
  {
  move_right();
  location = 0;
  }
}

 void ir_right_read(){


      
   while(digitalRead(ir_right)==0){
       
           
           if (digitalRead(ir_right)==1)
           {
          
             break;
           }
         }


 }
 void ir_left_read(){


      
   while(digitalRead(ir_left)==0){
       
           
           if (digitalRead(ir_left)==1)
           {
          
             break;
           }
         }


 }