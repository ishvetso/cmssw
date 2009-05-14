/*
 * =====================================================================================
 *
 *       Filename:  CSCDQM_Utility.h
 *
 *    Description:  CSC Utilities class
 *
 *        Version:  1.0
 *        Created:  10/30/2008 04:40:38 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Valdas Rapsevicius (VR), valdas.rapsevicius@cern.ch
 *        Company:  CERN, CH
 *
 * =====================================================================================
 */

#ifndef CSCDQM_Utility_H
#define CSCDQM_Utility_H

#include <string>
#include <map>
#include <set>
#include <vector>
#include <sstream>

#include <xercesc/util/XMLString.hpp>
#include <boost/shared_ptr.hpp>
#include <TString.h>
#include <TPRegexp.h>

namespace cscdqm {

  /**
  * @brief  Converting from whatever to string (failsafe!) 
  * @param  t whatever
  * @return result string
  */
  template <class T>
  const std::string toString(T& t) {
    std::ostringstream st;
    st << t;
    std::string result = st.str();
    return result;
  }

  /**
  * @brief  Converting from string to whatever number (failsafe!) 
  * @param  t result number
  * @param  s source string
  * @param  f base
  * @return true if success, else - false
  */
  template <class T>
  bool stringToNumber(T& t, const std::string& s, std::ios_base& (*f)(std::ios_base&)) {
    std::istringstream iss(s);
    return !(iss >> f >> t).fail();
  }

  /**
   * @class Utility
   * @brief General and CSCDQM Framework related utility routines
   */
  class Utility {

    public:

      static const bool regexMatch(const TPRegexp& re_expression, const std::string& message);
      static const bool regexMatch(const std::string& expression, const std::string& message);

      static const int getCSCTypeBin(const std::string& cstr);
      static const std::string getCSCTypeLabel(int endcap, int station, int ring);
      static const int tokenize(const std::string& str, std::vector<std::string>& tokens, const std::string& delimiters = " ");
      static void splitString(std::string str, const std::string delim, std::vector<std::string>& results);
      static void trimString(std::string& str);
      static uint32_t fastHash(const char * data, int len);
      static uint32_t fastHash(const char * data) { return fastHash(data, strlen(data)); }

  };


#define XERCES_TRANSCODE(str) cscdqm::XercesStringTranscoder(str).unicodeForm()

  /**
  * @class XercesStringTranscoder
  * @brief This is a simple class that lets us do easy (though not terribly
  * efficient) trancoding of char* data to XMLCh data.
  */
  class XercesStringTranscoder {

    public :

      XercesStringTranscoder(const char* const toTranscode) {
        fUnicodeForm = XERCES_CPP_NAMESPACE::XMLString::transcode(toTranscode);
      }

      ~XercesStringTranscoder() {
        XERCES_CPP_NAMESPACE::XMLString::release(&fUnicodeForm);
      }

      const XMLCh* unicodeForm() const {
        return fUnicodeForm;
      }

    private :

      XMLCh* fUnicodeForm;

  };

}

#endif
