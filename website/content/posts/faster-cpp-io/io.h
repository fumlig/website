///
/// \file io.h
/// \brief IO functions
///
/// Functions for IO, focused on speed. This is achieved by specializing each
/// function for the type it works with.
///
/// \author Oskar Lundin (olundin)
///

#include <cstdio>

#ifdef _WIN32
#define O_GETCHAR() _getchar_nolock()
#define O_PUTCHAR(c) _putchar_nolock(c)
#endif
#ifdef __linux__
#define O_GETCHAR() getchar_unlocked()
#define O_PUTCHAR(c) putchar_unlocked(c)
#endif

namespace o {

///
/// \brief Scans a character from stdin
/// \return The character scanned from stdin
///
inline char get_char() {
  return O_GETCHAR();
}

///
/// \brief Appends a character to stdout
/// \param c The character to append to stdout
///
inline void put_char(char c) {
  O_PUTCHAR(c);
}


///
/// \brief Scans an integer from stdin
///
/// Scans an integer from standard input (stdin). Assumes that the integer
/// is at the beginning of the input stream, with no whitespaces before it.
/// Stops scanning when a character which isn't a number is encountered. This
/// character is removed from the stream.
///
/// \tparam T Integer type (must be either char, int, short or long)
/// \return The integer scanned
///
template <typename T>
inline T scan_int() {
  T n = 0;
  bool negative = false;
  char c = get_char();
  // check if negative
  if(c == '-') {
    negative = true;
    c = get_char();
  }
  // scan digits
  do {
    n = n * 10 + c - '0';
    c = get_char();
  } while(c >= '0' && c <= '9');
  // negate if negative
  if(negative)
    n = -n;
  return n;
}
/// Explicit instantiation of scan_int for type int
template int scan_int<int>();

///
/// \brief Tries to scan an integer from stdin
///
/// Tries to scan an integer from standard input (stdin). If the first
/// character is not a number, it will stop scanning and return false.
/// Otherwise, the scan is continued until a character which isn't a number is
/// encountered. This character is removed from the stream and the function
/// returns true.
///
/// \tparam T Integer type (must be either char, int, short or long)
/// \param n The integer to set
/// \return True if the scan was successful, else false
///
template <typename T>
inline bool try_scan_int(T& n) {
  char c = get_char();
  if(c < '0' || c > '9')
    return false;
  ungetc(c, stdin);
  n = scan_int<T>();
  return true;
}

/// Explicit instantiation of scan_int_check for type int
template bool try_scan_int<int>(int&);

///
/// \brief Prints an integer to stdout
/// \tparam T Integer type (must be either char, int, short or long)
/// \tparam N Maximum number of digits in integer
/// \param n The integer to print
///
template<typename T, size_t N>
inline void print_int(T n) {
  if(n == 0) {
    put_char('0');
  } else {
  // check if negative
    if(n < 0) {
      put_char('-');
      n = -n;
    }
    // max number of digits is N
    char buffer[N];
    int i = N - 1;
    // scan digits and store
    while(n) {
      buffer[i--] = n % 10 + '0';
      n /= 10;
    }
    // print each digit
    while(i != N - 1) {
      put_char(buffer[++i]);
    }
  }
}
/// Explicit instantiation of scan_int_check for type int
template void print_int<int, 10>(int);

///
/// \brief Scans a string from stdin
///
/// Scans a string standard input (stdin) until the delimiter \p d is reached.
/// If the first character in stdin is EOF, the function stops scanning and
/// returns false. Otherwise characters are stored in \p s until the delimiter
/// is encountered and true is returned.
///
/// \param s String to fill with characters
/// \return True if the scan was successful, else false
///
inline bool scan(char* s, char d = ' ') {
  char c = get_char();
  if(c == EOF)
    return false;
  int index = 0;
  do {
    s[index++] = c;
    c = get_char();
  } while(c != d);
}

///
/// \brief Scans an entire line from stdin
///
/// Calls \ref scan "scan(s, '\n')".
///
/// \param s String to fill with characters
/// \return True if the scan was successful, else false
///
inline bool scanln(char* s) {
  return scan(s, '\n');
}

///
/// \brief Prints a string to stdout
/// \param s String to print
///
inline void print(const char* s) {
    int c = 0;
    while(s[c] != '\0')
        put_char(s[c++]);
}

///
/// \brief Prints a string to stdout and end line
/// \param s String to print
///
inline void println(const char* s) {
    print(s);
    put_char('\n');
}

}