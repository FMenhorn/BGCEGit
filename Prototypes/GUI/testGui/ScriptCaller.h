#ifndef SCRIPTCALLER_H
#define SCRIPTCALLER_H

class ScriptCaller
{
public:

void callScript(const std::string parameter)
 {
    std::system(parameter.c_str());
 }
};

#endif // SCRIPTCALLER_H
