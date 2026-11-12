#include <stdio.h>

/* 本人学号为 2026010030，数组十个元素按顺序对应学号的十位数字。 */
int main(void) {
    printf("Hello World\n");
    printf("Student ID: 2026010030\n");

    int number = 7;
    int student_id[10] = {2, 0, 2, 6, 0, 1, 0, 0, 3, 0};

    printf("number = %d\n", number);
    printf("Array ID: ");
    printf("%d", student_id[0]);
    printf("%d", student_id[1]);
    printf("%d", student_id[2]);
    printf("%d", student_id[3]);
    printf("%d", student_id[4]);
    printf("%d", student_id[5]);
    printf("%d", student_id[6]);
    printf("%d", student_id[7]);
    printf("%d", student_id[8]);
    printf("%d", student_id[9]);
    printf("\n");

    return 0;
}
