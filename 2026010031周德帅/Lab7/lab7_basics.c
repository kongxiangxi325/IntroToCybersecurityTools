#include <stdio.h>


int compare(int input1, int input2) {
    printf("hello world function\n");
    if (input1 < input2) {
        return input2;
    }else(input1 > input2);
    {
        return input1;
    }
}


/* 示例学号为 2026010099。练习时替换字符串和数组中的学号。 */
int main(void) {
    int result = compare(20,9);
    printf("result = %d\n", result);


    printf("Hello World\n");
    printf("Student ID: 2026010031\n");

    int number = 1024;
    int student_id[10] = {2, 0, 2, 6, 0, 1, 0, 0, 3, 1};

    printf("number = %d\n", number);
    // printf("Array ID: ");
    // printf("%d", student_id[0]);
    // printf("%d", student_id[1]);
    // printf("%d", student_id[2]);
    // printf("%d", student_id[3]);
    // printf("%d", student_id[4]);
    // printf("%d", student_id[5]);
    // printf("%d", student_id[6]);
    // printf("%d", student_id[7]);
    // printf("%d", student_id[8]);
    // printf("%d", student_id[9]);
    // printf("\n")；

    for  (int i = 0; i < 10; i++) {
        printf("%d \n", student_id[i]);
    }

int value = 9;
    printf("before %d \n", value);

    int *adress= &value;
*adress = 10;
    printf("after %d \n", *adress);




    return 0;
}
