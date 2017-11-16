/********************************************************************************
 * Data Structures in C++
 * Wangzhe, ahuwang@163.com
 * Copyright (c) 2017. All rights reserved.
 *******************************************************************************/

#pragma once

template <typename T> T& Vector<T>::operator[] ( Rank r ) const //重载下标操作符
{ return _elem[r]; }    //assert: 0 <= r < _size
