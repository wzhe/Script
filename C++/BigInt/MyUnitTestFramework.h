#ifndef __UNITTESTFRAME_H_
#define __UNITTESTFRAME_H_

// Use the method by vczh(http://www.cppblog.com/vczh/archive/2010/06/27/118829.html)


#define TEST_CASE(name) \
class TestCase_##name   \
    {   \
    public: \
        TestCase_##name();  \
    } TestCase_##name##_Instance;    \
    TestCase_##name::TestCase_##name()


#define TEST_ASSERT(expression) \
    do  \
    {   \
        if (!(expression))  \
        {   \
            throw "Test assert fails."; \
        }   \
    }   \
    while (false)


#endif // #ifndef __UNITTESTFRAME_H_


/********************************************************************
vczh(http://www.cppblog.com/vczh/archive/2010/06/27/118829.html)
//如何制造崩溃呢？最简单的办法就是抛异常
#define TEST_ASSERT(e) do(if(!(e))throw "今晚没饭吃。";}while(0)

#define TEST_CASE(NAME)                                            \
         extern void TESTCASE_##NAME();                             \
         namespace vl_unittest_executors                            \
         {                                                          \
             class TESTCASE_RUNNER_##NAME                           \
             {                                                      \
             public:                                                \
                 TESTCASE_RUNNER_##NAME()                           \
                 {                                                  \
                     TESTCASE_##NAME();                             \
                 }                                                  \
             } TESTCASE_RUNNER_##NAME##_INSTANCE;                   \
         }                                                          \
         void TESTCASE_##NAME()
**************************************************************************/
/*************************************
   那我们来看看TEST_CASE(x){y}究竟会被翻译成什么代码：
 1 extern void TESTCASE_x();
 2 namespace vl_unittest_executors
 3 {
 4     class TESTCASE_RUNNER_x
 5     {
 6     public:
 7         TESTCASE_RUNNER_x()
 8         {
 9             TESTCASE_x();
10         }
11     } TESTCASE_RUNNER_x_INSTANCE;
12 }
13 void TESTCASE_x(){y}
*****************************************/