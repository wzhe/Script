/********************************************************************************
 * Data Structures in C++
 * Wangzhe, ahuwang@163.com
 * Copyright (c) 2017. All rights reserved.
 *******************************************************************************/

#pragma once

template <typename T>
T Vector<T>::remove ( Rank lo, Rank hi) { //删除区间[lo,hi)
    if ( lo == hi ) return 0; //出于效率考虑，单独处理退化情况
    while ( hi < _size )  _elem[lo++] = _elem[hi++]; //[hi, size)顺次前移hi-lo个单元
    _size = lo;
    shrink();   //若有必要，则缩容
    return hi-lo; // 返回被删除元素的数目
}
