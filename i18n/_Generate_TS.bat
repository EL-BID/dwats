@echo off
Rem para classes que usam o método tr()
pylupdate5 SaniBidStarSD.pro

Rem para classes que não herdam de QObject, ou precisaram criar o método translate por outro motivo.
pylupdate5 -verbose -tr-function translate SaniBidStarSD.pro
pause