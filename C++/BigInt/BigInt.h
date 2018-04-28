#ifndef BIGINT_H_
#define BIGINT_H_

#include <vector>
#include <iostream>


class Bigint
{
    //Input&Output
    friend std::istream &operator >> (std::istream &, Bigint &);
    friend std::ostream & operator<<(std::ostream &out,const Bigint &obj);
public:
    //Constructors
    Bigint();
    Bigint(char c);
    Bigint(unsigned char c);
    Bigint(int i);
    Bigint(unsigned int i);
    Bigint(long l);
    Bigint(unsigned long l);
    Bigint(long long);
    Bigint(unsigned long long);
    Bigint(const std::string&);
    Bigint(const Bigint& other);


    //Adding
    Bigint operator+(Bigint const &) const;
    Bigint &operator+=(Bigint const &);
    Bigint operator+(long long const &) const;
    Bigint &operator+=(long long);
    Bigint &operator++();   //前置++
    Bigint operator++(int);    //后置++

    //Subtraction
    Bigint operator-(Bigint const &) const;
    Bigint &operator-=(Bigint const &);
    Bigint &operator--();   //前置--
    Bigint operator--(int);    //后置--

    //Multiplication

    Bigint operator*(long long const &);
    Bigint operator*(int const &);
    Bigint &operator*=(int const &);

    Bigint operator*(Bigint const &);
    Bigint &operator*=(Bigint const &);

    //Compare
    bool operator<(const Bigint &) const;
    bool operator>(const Bigint &) const;
    bool operator<=(const Bigint &) const;
    bool operator>=(const Bigint &) const;
    bool operator==(const Bigint &) const;
    bool operator!=(const Bigint &) const;

    //Allocation
    Bigint &operator=(const long long &);
    Bigint operator-() const;
    Bigint operator+() const;

    bool IsPositive() const;

    //Access
    int operator[](int const &);

    //Helpers
    void clear();
    Bigint &abs();

    //Power
    Bigint &pow(int const &);

    //Trivia
    int digits() const;
    int trailing_zeros() const;

    int size() const;

    static const int kBase = 1000 * 1000 * 1000; //10^9, 1000000000
    static const int kOutWidth = 9;
private:
    bool positive_;
    std::vector<int> number_;

private:
    int segment_length(int) const;
    int compare(Bigint const &) const; //0 a == b, -1 a < b, 1 a > b
};

Bigint absBigint(Bigint);
std::string to_string(Bigint const &);
Bigint factorial(int);

#endif
