#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// typedef struct node *nodePtr;
// struct node{
//     int value;
//     nodePtr next;
// };
// typedef struct node node;


// struct Player{
//     int age;
// }; 

// int main(){
//     struct Player Player1;
//     Player1.age=123;

//     printf("%d", Player1.age);
// }

typedef char Name[12];

int main(){
    Name name;
    strcpy(name, "abel");

    printf("%s", name);
}