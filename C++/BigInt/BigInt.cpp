#ifdef _WINDOWS
#define _CRTDBG_MAP_ALLOC
#include <crtdbg.h>
#endif

#include "BigInt.h"

#include <stdlib.h>
#include <iomanip>      // std::setw


#define ISDIGIT(ch)         ((ch) >= '0' && (ch) <= '9')
#define ISDIGIT1TO9(ch)     ((ch) >= '1' && (ch) <= '9')

Bigint::Bigint():
    positive_(true){ number_.push_back(0); }

Bigint::Bigint(const Bigint &other) :
    positive_(other.positive_), number_(other.number_){}

Bigint::Bigint(char c) : 
    positive_(c >= 0)
{
    c = ::abs(c);
    number_.push_back(c);
}

Bigint::Bigint(unsigned char c) : 
    positive_(true)
{
    number_.push_back(c);
}

Bigint::Bigint(int i) : 
    positive_(i >= 0)
{
    i = ::abs(i);
    do{
        number_.push_back(i % kBase);
    }while(i /= kBase);
}

Bigint::Bigint(unsigned int i) : 
    positive_(true)
{
    do{
        number_.push_back(i % kBase);
    }while(i /= kBase);
}

Bigint::Bigint(long l) :
    positive_(l >= 0)
{
    l = ::abs(l);
    do{
        int i = l % kBase;
        number_.push_back(i);
    }while(l /= kBase);
}

Bigint::Bigint(unsigned long l) :
    positive_(true)
{
    do{
        int i = l % kBase;
        number_.push_back(i);
    }while(l /= kBase);
}

Bigint::Bigint(long long num) :
    positive_(num >= 0)
{
    num = ::abs(num);
    do{
        int i = num % kBase;
        number_.push_back(i);
    }while(num /= kBase);
}

Bigint::Bigint(unsigned long long num) :
    positive_(true)
{
    do{
        int i = num % kBase;
        number_.push_back(i);
    }while(num /= kBase);
}

Bigint& Bigint::operator=(const long long &num)
{
    positive_ = (num >= 0);
    number_.clear();
    long long tempnum = ::abs(num);
    do{
        int i = tempnum % kBase;
        number_.push_back(i);
    }while(tempnum /= kBase);
    return *this;
}

Bigint::Bigint(const std::string& str)
{
    positive_ = true;
    int len = str.length();
    if(len == 0)
    {
        positive_ = true;
        number_.push_back(0);
        return;
    }

    const char *p = str.c_str();
    const char *pstart = p;
    const char *pend = p + len - 1;
    if (*p == '-')
    {
        positive_ = false;
        p++;
    }
    else if(*p == '+')
    {
        positive_ = true;
        p++;
    }
    while (*p == '0') p++;
    if (!ISDIGIT1TO9(*p))
    {
        positive_ = true;
        number_.push_back(0);
        return;
    }
    pstart = p;
    for (p++; ISDIGIT(*p); p++);
    pend = p;
    while(pend - pstart > Bigint::kOutWidth)
    {
        std::string strnum(pend-Bigint::kOutWidth, Bigint::kOutWidth);
        int num = stoi(strnum);
        //std::cout << "strnum:" << strnum << " num: " << num << std::endl;
        pend -= Bigint::kOutWidth;
        number_.push_back(num);
    }
    std::string strnum(pstart, pend);
    int num = stoi(strnum);
    pend -= Bigint::kOutWidth;
    number_.push_back(num);
}


int Bigint::size() const
{
    return number_.size();
}

bool Bigint::IsPositive() const
{
    return positive_;
}

Bigint Bigint::operator-() const
{
    Bigint result(*this);
    result.positive_ = !result.positive_;
    return result;
}

Bigint Bigint::operator+() const
{
    Bigint result(*this);
    result.positive_ = true;
    return result;
}

Bigint& Bigint::abs()
{
    positive_ = true;
    return *this;
}


Bigint absBigint(Bigint const &other)
{
    Bigint result(other);
    result.abs();
    return result;
}

Bigint & Bigint::operator+=(long long num)
{
    Bigint bigint(num);
    *this += bigint;
    return *this;
}


std::ostream & operator<<(std::ostream &out,const Bigint &obj)
{
    if(obj.size() == 0)
    {
        //std::cout << "nothing " << std::endl;
        out << "0";
        return out;
    }

    if(!obj.positive_)
    {
        out << "-";
    }

    auto it = obj.number_.crbegin();
    out << *it;
    while(++it != obj.number_.crend())
    {
        //out << " "; // for debug
        out << std::setfill('0') << std::setw(Bigint::kOutWidth) << *it;
    }
    return out;
}

bool Bigint::operator==(const Bigint &other) const
{
    //std::cout << *this << " VS " <<  other << std::endl;   //for debug
    if(positive_ != other.positive_) return false;
    if(size() != other.size()) return false;
    for(auto ithis = number_.cbegin(), ithat = other.number_.cbegin(); ithis != number_.cend(); ++ithis, ++ithat)
    {
        if(*ithis != *ithat)
            return false;
    }
    return true;
}
bool Bigint::operator!=(const Bigint &other) const
{
    return !(*this == other);
}

bool Bigint::operator<=(const Bigint &other) const
{
    //std::cout << *this << " <= " << other << std::endl;
    return !(*this > other);
}

bool Bigint::operator>=(const Bigint &other) const
{
    return (*this == other)||(*this > other) ;
}

bool Bigint::operator<(const Bigint &other) const
{
    return !(*this > other) && (*this != other);
}

bool Bigint::operator>(const Bigint &other) const
{
    if(positive_ != other.positive_)
    {
        return positive_;
    }

    if(size() != other.size())
    {
        if(positive_) return size() > other.size();
        else return other.size() > size();
    }

    for(auto ithis = number_.crbegin(), ithat = other.number_.crbegin(); ithis != number_.crend(); ++ithis, ++ithat)
    {
        if(*ithis == *ithat)
            continue;
        else
            return *ithis > *ithat;
    }
    return false;
}

void Bigint::clear()
{
    number_.clear();
}

Bigint Bigint::operator+(const Bigint &other) const
{
    Bigint result(*this);
    result += other;
    return result;
}
Bigint& Bigint::operator++()
{
    *this += 1;
    return *this;
}
Bigint Bigint::operator++(int n)
{
    Bigint result(*this);
    *this += 1;
    return result;
}



Bigint& Bigint::operator-=(Bigint const &other)
{
    Bigint tmpsub = -other;
    *this += tmpsub;
    return *this;
}


Bigint Bigint::operator-(const Bigint &other) const
{
    Bigint result(*this);
    result -= other;
    return result;
}
Bigint& Bigint::operator--()
{
    *this -= 1;
    return *this;
}
Bigint Bigint::operator--(int n)
{
    Bigint result(*this);
    *this -= 1;
    return result;
}



Bigint Bigint::operator*(long long const &longnum)
{
    Bigint result(longnum);
    result *= *this;
    return result;
}

Bigint Bigint::operator*(Bigint const &other)
{
    Bigint result(other);
    result *= *this;
    return result;
}

Bigint Bigint::operator*(int const &num)
{
    Bigint result((long long)num);
    result *= *this;
    return result;
}

Bigint& Bigint::operator*=(int const &num)
{
    Bigint that(num);
    *this *= that;
    return *this;
}

Bigint &Bigint::operator+=(const Bigint &other)
{
    while(other.size() > size())
    {
        number_.push_back(0);
    }
    if(other.positive_ == positive_)
    {
        int carry = 0;
        auto ithis = number_.begin();
        for(auto ithat = other.number_.cbegin() ; ithat != other.number_.cend(); ++ithis, ++ithat)
        {
            int sumofint = *ithis + *ithat + carry;
            if(sumofint >= kBase)
            {
                carry = sumofint / kBase;
                sumofint %= kBase;
            }
            else
            {
                carry = 0;
            }
            *ithis = sumofint;
        }

        if(carry)
        {
            if(ithis != number_.end())
            {
                *ithis += carry;
            }
            else
            {
                number_.push_back(carry);
            }
        }
        
    }
    else
    {
        this->abs();
        Bigint absother(other);
        absother.abs();
        Bigint *bigone = this;
        Bigint const *smallone = &absother;
        if( *this > absother )
        {
            positive_ = !other.positive_;
        }
        else
        {
            bigone = &absother;
            smallone = this;
            positive_ = other.positive_;
        }

        auto ibig = bigone->number_.begin();
        int borrow = 0;
        for(auto ismall = smallone->number_.cbegin(); ismall != smallone->number_.cend(); ++ibig, ++ismall)
        {
            int subofint = *ibig - *ismall - borrow;
            if(subofint < 0)
            {
                borrow = 1;
                subofint += kBase;
            }
            else
            {
                borrow = 0;
            }
            *ibig = subofint;
        }
        number_ = bigone->number_;
    }
    //https://stackoverflow.com/questions/1830158/how-to-call-erase-with-a-reverse-iterator
    auto itzeor= number_.end();
    while(itzeor != number_.begin())
    {
        itzeor--;
        if(*itzeor == 0)
        {
             itzeor = number_.erase(itzeor);
        }
        else
        {
            break;
        }
    }

    if(number_.size() == 0)
    {
        number_.push_back(0);
        positive_ = true;
    }
    return *this;
}

Bigint &Bigint::operator*=(const Bigint &other)
{

    Bigint zeor;
    if(*this == zeor || other == zeor)
    {
        *this = zeor;
        //std::cout << " zero " << std::endl;
        return *this;
    }

    Bigint const *bigone = this;
    Bigint const *smallone = &other;
    if( +(*this) <= +other )
    {
        bigone = &other;
        smallone = this;
    }

    Bigint result;
    result.number_.reserve(size() + other.size());
    int digit = 0;
    for(auto ismall = smallone->number_.cbegin(); ismall != smallone->number_.cend(); ++ismall, ++digit)
    {
        int carry = 0;
        Bigint temresult;
        temresult.clear();
        temresult.number_.reserve(size() + other.size());
        for(auto i = 0; i < digit; ++i)
        {
            //std::cout << "push_back 0:" << digit << std::endl;
            temresult.number_.push_back(0);
        }
        for(auto ibig = bigone->number_.cbegin(); ibig != bigone->number_.cend(); ++ibig)
        {
            long long int mulofint = static_cast<long long int>(*ibig) * (*ismall) + carry;
            //std::cout << *ibig  << " * " <<  *ismall << "== " << mulofint << std::endl;
            if(mulofint >= kBase)
            {
                carry = mulofint / kBase;
                mulofint %= kBase;
            }
            else
            {
                carry = 0;
            }
            temresult.number_.push_back(mulofint);
        }
        if(carry)
        {
            //std::cout << "push_back carry:" << carry << std::endl;
            temresult.number_.push_back(carry);
        }
        //std::cout << "temresult:" << temresult << std::endl;
        result += temresult;
    }
    if(other.positive_ == positive_)
    {
        result.positive_ = true;
    }
    else
    {
        result.positive_ = false;
    }
    //std::cout << "result:" << result << std::endl;
    *this = result;

    return *this;
}


//1000000000
//9223372036854775807
