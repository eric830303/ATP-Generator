from protocol import *
#---------------------------------------------------------------------
class I2C( Protocol ):
    def __init__( self, name ):
        Protocol.__init__( self, name )
    def cSet_RW_Format( self, cmd ):
        _Set_RW_Format( self, cmd )
    def cSet_Reg_Addr(self):
        _Set_Reg_Addr(self)
    def cSet_Port_Value(self):
        _Set_Port_Value(self)
    def cSet_RW_Data(self):
        _Set_RW_Data(self)
    def cSet_Start( self ):
        _Set_Start( self )
    def cSet_End( self ):
        _Set_End( self )
    def cSet_Ctrl_Byte( self, ctrl, rw ):
        _Set_Ctrl_Byte( self, ctrl, rw )
#---------------------------------------------------------------------
def _Set_RW_Format( self, cmd ):
    if ( cmd.COMMAND not in self.cmd_list ) or ( not self.ifdo ):
        return
    else:
        ctrl = self.args.ctrlbyte #Ctrl byte
        #--Start------------------
        self.cSet_I2C_Start()
        #--Ctrl byte--------------
        self.cSet_I2C_Ctrl_Byte( ctrl, "w" )
        #--Write Reg Addr---------
        self.cSet_I2C_Reg_Addr( cmd )
        if "R" in cmd.COMMAND:
            #--Set Start--------------
            self.cSet_I2C_SCL_SDA( 0, 1 )
            self.cSet_I2C_SCL_SDA( 1, 0 )
            #--Ctrl byte--------------
            self.cSet_I2C_Ctrl_Byte( ctrl, "r" )
        #--RW Data-------------
        self.cSet_I2C_RW_Data( cmd )
        #--End---------------------
        self.cSet_I2C_End()
