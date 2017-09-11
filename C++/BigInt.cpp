#ifdef _WINDOWS
#define _CRTDBG_MAP_ALLOC
#include <crtdbg.h>
#endif
#include "BigInt.h"

Bigint::Bigint() :
	positive(true), base(Bigint::default_base), skip(0) {}

Bigint::Bigint(const Bigint &other) :
	positive(other.positive), number(other.number), base(other.base), skip(other.skip) {}

Bigint::Bigint(long long a) :
{
	if (a >= 0) {
		positive = true;
	}
	else {
		a *= -1;
		positive = false;
	}
	base = Bigint::default_base;
	skip = 0;
	while (a) {
		number.push_back((int)(a % base));
		a /= base;
	}
}
#define ISDIGIT(ch)         ((ch) >= '0' && (ch) <= '9')
#define ISDIGIT1TO9(ch)     ((ch) >= '1' && (ch) <= '9')
Bigint::Bigint(std::string s) :{
	positive = true;
	skip = 0;
	base = Bigint::default_base;
	if (s.length = 0) {
		number.push_back(0);
	}
	else {
		auto c = s.cbegin();
		if (*c == '-') {
			positive = false;
			c++;
		}
		while (*c == '0') *c++;
		if (ISDIGIT1TO9(*c)) {
			Bigint a = *c;
			while (c != s.cend() && ISDIGIT(*c)) {
				a = a * 10 + *c;
			}
			number = a.number;
		}
		else {
			throw ("Error, can not transform %c to Bigint ", *c);
		}
	}
}

Bigint Bigint::operator+(const Bigint &lhs) const
{

}

Bigint& Bigint::operator+=(Bigint const &rhs) {


}
