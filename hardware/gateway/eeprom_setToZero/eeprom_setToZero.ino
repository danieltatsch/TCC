#include <EEPROM.h>

/*Tamanho definido de quantos bytes foram utilizados
   - Caso queria verificar toda a memoria -> EEPROM.length() 
   - senão, colocar somente uma estimativa de quantos
     bytes foram usados
*/
#define EEPROM_SIZE 10


int readMemory(int addr){
  return EEPROM.read(addr);
}

void writeMemory(int addr, int value){
  EEPROM.write(addr, value);
  EEPROM.commit();
  delay(1000); //Operacao de escrita demora aprox 3.3ms
//  Serial.println("Valor de counter salvo na memoria");
}

void setup(){
  Serial.begin(115200);
  EEPROM.begin(EEPROM_SIZE);
  
  Serial.println("Dados atuais...\n");
  for (int i = 0; i < EEPROM_SIZE; i++){
    Serial.print(int(readMemory(i)));
    if (i < EEPROM_SIZE - 1) Serial.print(", ");
  }
  
  Serial.println("\n\nConfiguando memoria...\n");
  
  for (int i = 0; i < EEPROM_SIZE; i++){
    int aux = readMemory(i);
    if (aux == 0 || aux == 255){
      Serial.print("Dado ja zerado ou nao modificado, ignorando posicao: ");
      Serial.println(i);
      continue;
    }
    writeMemory(i, 0);
  }

  Serial.println("\nMemoria configurada, verificando posicoes...\n");
  delay(1000);

  for (int i = 0; i < EEPROM_SIZE; i++){
    Serial.print(int(readMemory(i)));
    if (i < EEPROM_SIZE - 1) Serial.print(", ");
  }
}

void loop(){
}

