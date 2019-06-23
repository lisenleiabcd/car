#define LEFT_AHEAD 10
#define LEFT_BACK 9
#define RIGHT_AHEAD 12
#define RIGHT_BACK 13
/*#define STEER 14*/
int duty = 1230;
String inString="";
float RunInit = 3.0;
float RUN_LEFT = 3.0;
float RUN_RIGHT = 3.0;

int TURN = 150;
int RUN1 = 255;
int CYC = 5;
float calibrateNum = 0;
void stopBack();
void turnLeft();
void turnRight();
void goAhead();
void park();
void goBack();

void setup(){
    Serial.begin(9600);
    pinMode(LEFT_AHEAD,OUTPUT);
    pinMode(LEFT_BACK, OUTPUT);
    pinMode(RIGHT_AHEAD, OUTPUT);
    pinMode(RIGHT_BACK, OUTPUT);
    digitalWrite(LEFT_AHEAD, LOW);
    digitalWrite(LEFT_BACK, LOW);
    digitalWrite(RIGHT_AHEAD, LOW);
    digitalWrite(RIGHT_BACK, LOW);
  
}

char incomingByte = ' ';

void loop(){
    if (Serial.available() > 0) {
        // read the incoming byte:
        incomingByte = Serial.read();
        if (incomingByte == 'L') {
            Serial.println("TURN LEFT");
            turnLeft();
            Serial.read();
        } else if (incomingByte == 'R'){
            Serial.println("TURN RIGHT");
            turnRight();
            Serial.read();
        } else if (incomingByte == 'A'){
            Serial.println("GO AHEAD");
            goAhead();
            Serial.read();
        } else if (incomingByte == 'B'){
            Serial.println("GO BACK");
            goBack();
            Serial.read();
        } else if (incomingByte == 'P'){
            Serial.println("PARK");
            park();
            Serial.read();
        } 
        
    }
}


void goAhead(){
    stopBack();
    analogWrite(LEFT_AHEAD,TURN);  
    analogWrite(RIGHT_AHEAD,TURN);
}

void turnLeft(){
    stopBack();
    analogWrite(RIGHT_AHEAD,TURN);
    digitalWrite(RIGHT_BACK,LOW);
    analogWrite(LEFT_BACK,TURN);
    digitalWrite(LEFT_AHEAD,LOW);
}

void turnRight(){
    stopBack();
    analogWrite(LEFT_AHEAD,TURN);
    digitalWrite(LEFT_BACK,LOW);
    analogWrite(RIGHT_BACK,TURN);
    digitalWrite(RIGHT_AHEAD,LOW);
}

void park(){
    stopBack();
    digitalWrite(LEFT_AHEAD, LOW);
    digitalWrite(RIGHT_AHEAD, LOW);
    //steer(1);
}

void goBack(){
    digitalWrite(LEFT_AHEAD,LOW);
    digitalWrite(RIGHT_AHEAD,LOW);
    analogWrite(LEFT_BACK,RUN1);
    analogWrite(RIGHT_BACK,RUN1);  
}

void stopBack(){
    digitalWrite(LEFT_BACK, LOW);
    digitalWrite(RIGHT_BACK, LOW);
}
/*used to integer input
int readInt(){
  int x;
  int flag=1;
  while(flag){
    while (Serial.available() > 0) {
      int inChar = Serial.read();
      if (isDigit(inChar)) {
        // convert the incoming byte to a char 
        // and add it to the string:
        inString += (char)inChar; 
      }
      // if you get a newline, print the string,
      // then the string's value:
      if (inChar == '\n') {
        x=inString.toInt();
        flag=0;
        // clear the string for new input:
        inString = ""; 
      }
    }
  }
  return x;
}
*/