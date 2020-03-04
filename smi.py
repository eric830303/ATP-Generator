from protocol import *
#---------------------------------------------------------------------
class SMI( Protocol ):
    def __init__( self, name ):
        Protocol.__init__( self, name )
    def cSet_RW_Format( self, format ):
        _Set_RW_Format( self, format )
    def cSet_Reg_Addr(self):
        _Set_Reg_Addr(self)
    def cSet_Port_Value(self):
        _Set_Port_Value(self)
    def cSet_RW_Data(self):
        _Set_RW_Data(self)
