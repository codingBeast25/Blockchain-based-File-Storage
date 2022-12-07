/*
Name : Bhautik Sojitra
Student Id: 7900140
Course: Introduction to Cryptography and CryptoSystems (COMP 4140)
Assignment #3
Purpose: Build an AES encryption and decryption scheme 
*/

#include <iostream>
#include <iomanip>
#include <sstream>
#include <fstream>
#include <string>

#include "AES.h"

using namespace std;

// creates 2D array pf given size
uint8_t **create2DArray(int rows, int cols )
{
    uint8_t **new_state = new uint8_t*[rows];

    for(int i = 0; i < rows; i++)
    {
        new_state[i] = new uint8_t[cols];

        for(int j = 0 ; j < cols; j++)
        {
            new_state[i][j] = 0; // assigns the value to be zero for all elements
        }
    }

    return new_state;
}

// removes 2D array object after use and clean the memory
void cleanUpMemory(uint8_t **to_remove , int rows, int cols)
{
    
    for (int i = 0; i < rows; i++) // loop variable wasn't declared
    {
        delete [] to_remove[i];
    }
    delete [] to_remove;
    to_remove = 0;
          
}


// This function changes the state array using sbox array values.
uint8_t  **SubBytes(uint8_t **state, int rows, int cols)
{
   
    uint8_t **new_state = create2DArray(rows , cols);

    for(int i = 0 ; i < rows ; i++)
    {
        for(int j = 0 ; j  < cols ; j++)
        {
            new_state[i][j] = sbox[state[i][j]]; 
        }
    
    }

    cleanUpMemory(state, rows, cols);
    return new_state;

}

// It changes state array by shifting elements in each row by row_number time. 
uint8_t **ShiftRows(uint8_t **state, int rows, int cols)
{
    uint8_t **new_state = create2DArray(rows , cols);
    
    for(int i = 0 ; i < rows ; i++)
    {
        for(int j = 0; j < cols ; j++)
        {
            new_state[i][j] = state[i][(j+i)%cols];
        }

    }

    cleanUpMemory(state, rows, cols);
    return new_state;
 
}

// does cyclic rotate on a 32 bit int value 
uint32_t CyclicLeftRotate(uint32_t value , int bits_to_shift)
{
    return (value << bits_to_shift) | (value >> (32 - bits_to_shift));
}

// substitute 32 bit int value using sbox array values for key expansion 
uint32_t subBytes32(uint32_t value)
{
    uint32_t result;
    
    uint8_t c[4];

    for(int j = 0 ; j < 4 ; j++)
    {
        c[j] = value >> 32 - 8*(j+1);
        c[j] = sbox[c[j]];
    }

    for(int j = 0 ; j < 4 ; j++)
    {
        result = result | (static_cast <uint32_t>(c[j])) << 32 - 8*((j)+1);  
    }
    
    return result;
}


// given a 128 bit key, it creates an array of 11 128-bit different keys
uint8_t** KeyExpansion(uint8_t key[16])
{
    
    uint32_t **key_array = new uint32_t*[11]; // 2D array for 11 keys divided into 32 bit chuncks 
    uint8_t **key_array_to_return = new uint8_t*[11]; // 2D array for 11 keys divided into 8 bit chuncks

    // sets the values for 2D array to be zero. 
    for(int i = 0; i < 11; i++)
    {
        key_array[i] = new uint32_t[4];

        for(int j = 0 ; j < 4; j++)
        {
            key_array[i][j] = 0;
        }
    }

    // sets the value for 2d array to be zero.
    for(int i = 0; i < 11; i++)
    {
        key_array_to_return[i] = new uint8_t[16];

        for(int j = 0 ; j < 16; j++)
        {
            key_array_to_return[i][j] = 0;
        }
    }

    // sets the first key among 11 keys to be an original key
    for(int i = 0 ; i < 4 ; i++)
    {
        for(int j = 4*i ; j < 4*i+ 4 ; j++)
        {
            // doing 8-bit to 32-bit conversion
            key_array[0][i] = key_array[0][i] | (static_cast <uint32_t>(key[j])) << 32 - 8*((j%4)+1);  
        }
    }

    // calculating 10 more keys using XOR, cyclicRotate and sbox substitution
    for(int i = 1 ; i < 11 ; i++)
    {
        uint32_t rotated = CyclicLeftRotate(key_array[i-1][3] , 8);
        cout << "" << flush;
        uint32_t substituted = subBytes32(rotated);
        cout << "" << flush;
        key_array[i][0] = key_array[i-1][0] ^ substituted ^ c[i-1];
        key_array[i][1] = key_array[i-1][1] ^ key_array[i][0] ;
        key_array[i][2] = key_array[i-1][2] ^ key_array[i][1];
        key_array[i][3] = key_array[i-1][3] ^ key_array[i][2];
    }

    
    // print all keys one per line in 32-bit chunck
    for(int i = 0 ; i < 11 ; i++)
    {
        for(int j = 0;  j < 4; j++)
        {
            cout << hex << key_array[i][j] << ",";
        }
        cout << endl;
    }

    // converting keys with 32-bit chuncks to keys with 8-bit chuncks.
    for(int k = 0 ; k < 11 ; k++)
    {
        for(int i = 0; i < 4; i++)
        {
            for(int j = 0 ; j < 4 ; j++)
            {
                key_array_to_return[k][4*i + j] =  key_array[k][i] >> 32 - 8*(j+1);
                
            }
        }

    }

    return key_array_to_return;

}

// converts ascii into kex
int ascii_to_hex(char c)
{
    int num = (int) c;
    if(num < 58 && num > 47)
    {
        return num - 48; 
    }
    if(num < 103 && num > 96)
    {
        return num - 87;
    }
    return num;
}

// reading a file with hex data as a string form
uint8_t *ReadFile(string file_name, int size)
{
    uint8_t *in = new uint8_t[size]; // stores the output of file processing

    uint8_t hex_data;
    string line; 
    ifstream file_(file_name);
    
    if(file_.is_open())
    {
        int i = 0;
        if(getline(file_ , line))
        {
            stringstream ss(line);
            string final_string;
            string word;
            // reads each word from the file
            while(ss >> word)
            {
                final_string += word;
            }

            cout << final_string << endl;
            int j = 0;
            
            // converts each word to one 8 bit hex value
            while(i < final_string.length())
            {
                uint8_t c1 = ascii_to_hex(final_string[i++]);
                uint8_t c2 = ascii_to_hex(final_string[i++]);
                in[j++] =  c1 << 4 | c2 ;
                
            }
            
        }
        file_.close();
        
    }

    return in;

}

// it checks if the binary value only has 1 set bit or not
// 1 set bit means value is power of 2.
bool checkPower2(uint8_t value)
{
    int count = 0;
    for(int i = 0; i < 8 ; i++ )
    {
        uint8_t test = value & 0x01;

        if(test == 0x01)
        {
            count++;
        }

        value = value >> 1;

    }

    if(count == 1)
    {
        return true;
    }
    else
    {
        return false;
    }
}

// multiplys with 0x02 (if lsb is 1 for the value then after multiplying, we need to XOR with 0x1B for final result)
uint8_t multiplyWith02(uint8_t value)
{
    uint8_t lsb = value >> 7;

    value = value << 1;

    if(lsb == 1)
    {
        value = value ^ 0x1B;
    }

    return value;

}

// multiply with any value that is power 2 using recursion
uint8_t multiplyWithPower2(uint8_t value, uint8_t to_multiply)
{
    if(checkPower2(to_multiply))
    {
        if(to_multiply != 0x02)
        {
            to_multiply = to_multiply >> 1;
            value = multiplyWith02(value);
            return multiplyWithPower2(value, to_multiply);
        }
        else
        {
            return multiplyWith02(value);
        }
    }
    else
    {   
        cout << "Invalid value to multiply with " << endl;
        return -1;
    }
    
}

uint8_t *separateBitsForMixCols(uint8_t value )
{
    uint8_t *to_return = new uint8_t[8];

    for(int i = 0; i < 8; i++)
    {
        to_return[i] = 0;
    }
    
    uint8_t test_hex = 0x01;
    int count = 0;
    for(int i= 0 ; i < 8; i++)
    {
        if(value & test_hex)
        {
            to_return[count++] = test_hex;
        }

        test_hex = test_hex << 1;
    }

    return to_return;
}

uint8_t multiplyWithAnyHex(uint8_t value, uint8_t to_multiply)
{
    uint8_t result = 0;
    if(to_multiply != 0x02 && !checkPower2(to_multiply))
    {
        uint8_t *simplified_values = separateBitsForMixCols(to_multiply);

        
        for(int i =0 ; i < 8; i++)
        {
            if(simplified_values[i] != 0x01 && simplified_values[i] != 0x00)
            {
                result ^= multiplyWithPower2(value, simplified_values[i]);
            }
            else if(simplified_values[i] == 0x01)
            {
                result ^= value;
            }
        }

    }
    else if(to_multiply == 0x02)
    {
        result = multiplyWith02(value);
    }
    else
    {
        result = multiplyWithPower2(value, to_multiply);
    }

    return result;
}

uint8_t **MixCols(uint8_t **state, int rows, int cols)
{
    uint8_t **new_state = create2DArray(rows, cols);
    for(int j = 0; j < cols; j++)
    {
        uint8_t first_row = multiplyWith02(state[0][j]) ^ (multiplyWith02(state[1][j]) ^ state[1][j]) ^ state[2][j] ^ state[3][j];
        uint8_t second_row =  state[0][j] ^ multiplyWith02(state[1][j]) ^ (multiplyWith02(state[2][j]) ^ state[2][j]) ^ state[3][j];
        uint8_t third_row = state[0][j] ^ state[1][j] ^ multiplyWith02(state[2][j]) ^ (multiplyWith02(state[3][j]) ^ state[3][j]);
        uint8_t forth_row = (multiplyWith02(state[0][j]) ^ state[0][j]) ^ state[1][j] ^ state[2][j] ^ multiplyWith02(state[3][j]);

        new_state[0][j] = first_row;
        new_state[1][j] = second_row;
        new_state[2][j] = third_row;
        new_state[3][j] = forth_row;

    
    }
    cleanUpMemory(state, rows, cols);
    return new_state;
}

void print1DArray(uint8_t*  arr, int size)
{
    for(int i = 0 ; i < size; i++)
    {
        cout << hex << setw(2) << setfill('0') << +arr[i] << " ";
    }
    
    cout << endl;
}

void print2DArray(uint8_t**  arr, int rows, int cols)
{
    for(int i = 0 ; i < rows; i++)
    {
        for(int j = 0;  j < cols; j++)
        {
            cout << hex << setw(2) << setfill('0') << +arr[j][i] << " ";
        }
        cout << "\t";
    }

    cout << endl;
}

uint8_t *Encrypt(uint8_t* plainText, uint8_t* keyText)
{
    uint8_t *cipherText = 0;
    cipherText = new uint8_t[16];

    cout << "KeySchedule" << endl;
    uint8_t **k_arr = KeyExpansion(keyText);
    cout << endl;
    
    cout << endl;
    uint8_t result[16];
    for(int i = 0 ; i < 16 ; i++)
    {
        result[i] = plainText[i] ^ k_arr[0][i];
    }

    cout << "ENCRYPTION PROCESS" << endl;
    cout << "------------------" << endl;
    cout << endl;

    cout << "PlainText" << endl;
    print1DArray(plainText, 16);
    cout << endl;
    
    uint8_t **state = create2DArray(4, 4);

    for(int i = 0 ; i < 4 ; i++)
    {
        for(int j = 0 ; j  < 4 ; j++)
        {
            state[i][j] = result[i + 4*j];
             
        }
        
    }

    for(int r = 1; r < 11; r++)
    {
    
        state = SubBytes(state, 4, 4);
        state = ShiftRows(state,4,4);
        
        if(r <= 9){
            state = MixCols(state, 4, 4);
            cout << "State After Call " << r << " To MixCols" << endl;
            cout << "---------------------------------------" << endl;
            print2DArray(state,4,4);
            cout << endl;
        }

        
        for(int i = 0 ; i < 4 ; i++)
        {
            for(int j = 0 ; j  < 4 ; j++)
            {
                state[i][j] ^= k_arr[r][i + 4*j];
             
            }
        
        }


    }

    cout << "CipherText" << endl; 
    print2DArray(state,4,4);
    cout << endl;
    
    for(int i = 0 ; i < 4 ; i++)
    {
        for(int j = 0 ; j  < 4 ; j++)
        {
            cipherText[4*i + j] = state[j][i];
             
        }
        
    }

    cleanUpMemory(state, 4, 4);
    return cipherText;

}


//Decryption methods


uint8_t **InvSubBytes(uint8_t **state, int rows, int cols)
{
    uint8_t **new_state = create2DArray(rows, cols);

    for(int i = 0 ; i < rows ; i++)
    {
        for(int j = 0 ; j  < cols ; j++)
        {
            new_state[i][j] = invsbox[state[i][j]]; 
        }
    
    }

    cleanUpMemory(state, rows, cols);
    return new_state;


}

uint8_t **InvShiftRows(uint8_t **state, int rows, int cols)
{
    uint8_t **new_state = create2DArray(rows , cols);
    
    for(int i = 0 ; i < rows ; i++)
    {
        for(int j = 0; j < cols ; j++)
        {
            new_state[i][j] = state[i][(cols + (j-i))%cols];
        }

    }

    cleanUpMemory(state, rows, cols);
    return new_state;
}

uint8_t **InvMixCols(uint8_t **state, int rows, int cols)
{
    uint8_t **new_state = create2DArray(rows, cols);
    for(int j = 0; j < cols; j++)
    {
        uint8_t first_row = multiplyWithAnyHex(state[0][j] , 0x0E) ^ multiplyWithAnyHex(state[1][j] , 0x0B) ^ multiplyWithAnyHex(state[2][j] , 0x0D) ^ multiplyWithAnyHex(state[3][j] , 0x09);
        uint8_t second_row =  multiplyWithAnyHex(state[0][j] , 0x09) ^ multiplyWithAnyHex(state[1][j] , 0x0E) ^ multiplyWithAnyHex(state[2][j] , 0x0B) ^ multiplyWithAnyHex(state[3][j] , 0x0D);
        uint8_t third_row = multiplyWithAnyHex(state[0][j] , 0x0D) ^ multiplyWithAnyHex(state[1][j] , 0x09) ^ multiplyWithAnyHex(state[2][j] , 0x0E) ^ multiplyWithAnyHex(state[3][j] , 0x0B);
        uint8_t forth_row = multiplyWithAnyHex(state[0][j] , 0x0B) ^ multiplyWithAnyHex(state[1][j] , 0x0D) ^ multiplyWithAnyHex(state[2][j] , 0x09) ^ multiplyWithAnyHex(state[3][j] , 0x0E);

        new_state[0][j] = first_row;
        new_state[1][j] = second_row;
        new_state[2][j] = third_row;
        new_state[3][j] = forth_row;

    
    }
    cleanUpMemory(state, rows, cols);
    return new_state;

}

uint8_t *Decrypt(uint8_t* cipherText, uint8_t *keyText)
{
    uint8_t *plainText = 0;
    plainText = new uint8_t[16];

    cout << "KeySchedule" << endl;
    uint8_t **k_arr = KeyExpansion(keyText);
    cout << endl;
    
    cout << endl;

    uint8_t result[16];
    for(int i = 0 ; i < 16 ; i++)
    {
        result[i] = cipherText[i] ^ k_arr[10][i];
    }
    cout << "DECRYPTION PROCESS" << endl;
    cout << "------------------" << endl;
    cout << endl;

    cout << "CipherText" << endl;
    print1DArray(cipherText, 16);
    cout << endl;
    uint8_t **state = create2DArray(4, 4);

    for(int i = 0 ; i < 4 ; i++)
    {
        for(int j = 0 ; j  < 4 ; j++)
        {
            state[i][j] = result[i + 4*j];
             
        }
        
    }

    
    for(int r = 9 ; r >= 0 ; r--)
    {
        state = InvShiftRows(state,4,4);
        state = InvSubBytes(state, 4, 4);
        

        for(int i = 0 ; i < 4 ; i++)
        {
            for(int j = 0 ; j  < 4 ; j++)
            {
                state[i][j] ^= k_arr[r][i + 4*j];
                
            }
            
        }

        if(r > 0)
        {
            cout << "State After Call " << r << " To InvMixCols" << endl;
            cout << "---------------------------------------" << endl;
            state = InvMixCols(state, 4, 4);
            print2DArray(state,4,4);
            cout << endl;
        }
    }
     cout << "PlainText" << endl; 
     print2DArray(state,4,4);
     cout << endl;
    
    
        
    cleanUpMemory(state, 4, 4);
    return plainText;

}

int main(int argc, char *argv[]) {

    cout << "PlainText" << endl;
    uint8_t *plaintext = ReadFile(argv[1], 16);
    cout << "Key" << endl;
    uint8_t *keyText = ReadFile(argv[2], 16);

    uint8_t *cipher = Encrypt(plaintext, keyText);
    uint8_t *plain = Decrypt(cipher, keyText);
    

    return 0;
}




