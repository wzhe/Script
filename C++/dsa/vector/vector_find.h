/********************************************************************************
 * Data Structures in C++
 * Wangzhe, ahuwang@163.com
 * Copyright (c) 2017. All rights reserved.
 *******************************************************************************/

#pragma once

template <typename T>   //无序向量的顺序查找：返回最后一个元素的位置；失败时，返回lo-1
Rank Vector<T>::find ( T const& e, Rank lo, Rank hi ) const { //assert: 0 <= lo < hi <= _size
    while ( ( lo < hi-- ) && ( e != _elem[hi] ) ); //从后向前，顺序查找
    return hi;
}
