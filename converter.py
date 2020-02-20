#--------------------------------------------------------------------
#  Import API
#--------------------------------------------------------------------
import os
import pandas   as pd
import argparse as ag
#---------------------------------------------------------------------
class Port:
    def __init__( self, name, value ):
        self.name     = name
        self.value    = value
        self.protocol = ""
class converter:
    def __init__( self ):
        self.args        = ''
        self.unknown     = ''
        self.input       = ''
        self.df_port     = ''
        self.df_cmd      = ''
        self.vector      = []
        self.f           = ''

    #-----Parser-------------------------------------
    def cParseArgs( self ):
        _ParseArgs( self )
    def cParseDataFame( self ):
        _ParseDataFrame( self )
    def cGenATP( self ):
        _GenATP( self )
    def cGenVectorList( self ):
        return _GenVectorList( self )
    def cPutPortInVector( self, port_list, protocol, value ):
        _PutPortInVector( self, port_list, protocol, value )
    #-----Boot-Up-------------------------------------
    def cGenATP_Idle( self, cnt ):
        _GenATP_Idle( self, cnt )
    #-----I2C--------------------------------------
    def cSet_I2C_Format( self, cmd ):
        _Set_I2C_Format( self, cmd )
    def cSet_I2C_SCL_SDA( self, SCL, SDA ):
        _Set_I2C_SCL_SDA( self, SCL, SDA )
    def cSet_I2C_Start( self ):
        _Set_I2C_Start( self )
    def cSet_I2C_End( self ):
        _Set_I2C_End( self )
    def cSet_I2C_Ctrl_Byte( self, ctrl ):
        _Set_I2C_Ctrl_Byte( self, ctrl )
    def cSet_I2C_Reg_Addr( self, cmd ):
        _Set_I2C_Reg_Addr( self, cmd )
    def cSet_I2C_RW_Data( self, cmd ):
        _Set_I2C_RW_Data( self, cmd )
    #-----SPI--------------------------------------
    def cSet_SPI_Format( self, cmd ):
        _Set_SPI_Format( self, cmd )
    def cSet_SPI_SS_CLK_DI_DO( self, a, b, c, d ):
        _Set_SPI_SS_CLK_DI_DO( self, a, b, c, d )
    def cSet_SPI_Reg_Addr( self, cmd ):
        _Set_SPI_Reg_Addr( self, cmd )
    def cSet_SPI_RW_Data( self, cmd ):
        _Set_SPI_RW_Data( self, cmd )
    #----Basic--------------------------------------
    def cGenATPbyValue( self ):
        _GenATPbyValue( self  )
#----------------------------------------------------------------------------
def _ParseArgs( self ):
    example = "\
    Example: \n\
    (linux, macOS)        ./converter.py -input i2c_pattern.xlsx -output i2c_pattern.atp -i2c \n\
    (   Windows  ) python .\converter.py -input i2c_pattern.xlsx -output i2c_pattern.atp -i2c \n\
    "

    help_in    = "Your excel input"
    help_spi   = "Convert the SPI to ATP based on SPI protocol"
    help_i2c   = "Convert the I2C to ATP based on I2C protocol"
    help_out   = "Specify your output ATP filename"
    help_ctrl  = "Specify your I2c ctrl byte, 1010100 at default."
    parser     = ag.ArgumentParser( epilog=example, formatter_class=ag.RawTextHelpFormatter )
    parser.add_argument( "-input"               ,help=help_in        ,dest="infname"            ,default="" )
    parser.add_argument( "-spi"                 ,help=help_spi       ,dest="ifspi"              ,default=False          ,action="store_true")
    parser.add_argument( "-i2c"                 ,help=help_i2c       ,dest="ifi2c"              ,default=False          ,action="store_true")
    parser.add_argument( "-output"              ,help=help_out       ,dest="outfname"           ,default="output.atp")
    parser.add_argument( "-ctrlbyte"            ,help=help_out       ,dest="ctrlbyte"           ,default="1010100")
    self.args, self.unknown = parser.parse_known_args()
    #----------------Checker------------------------------------------
    if ( self.args.infname == "" ):
        print( "[Error] Your input excel file is not specify by arg -input" )
        exit(-1)
    if ( not self.args.ifi2c ) and ( not self.args.ifspi ):
        print( "[Error] One of args \"-spi\" or \"-i2c\" must be specidfied" )
        exit(-1)
    if ( self.args.ifi2c ) and ( self.args.ifspi ):
        print( "[Error] Only one of args \"-spi\" or \"-i2c\" can be specidfied" )
        exit(-1)
#----------------------------------------------------------------------------
def _PutPortInVector( self, port_list, protocol, value ):
    for p in port_list:
        if ( not pd.isna(p) ):
            p_inst = Port( p, value )
            if p_inst not in self.vector:
                p_inst.protocol = protocol
                self.vector.append( p_inst )
#----------------------------------------------------------------------------
def _ParseDataFrame( self ):
    try:
        self.df_port = pd.read_excel( self.args.infname, header=0, sheet_name="PORT" )
        self.df_cmd  = pd.read_excel( self.args.infname, header=0, sheet_name="CMD" )
        print( "[Info] Reading %s" % self.args.infname )
    except:
        print( "[Error] Fail to read excel" )
        print( "[Error] Input file must be *.xlsx format. Maybe your input is *.csv or other formates, which is not allowed" )
    #----------Parse Port Data---------------------------------------------
    self.cPutPortInVector( self.df_port[ "Tie-1 Port" ]  ,"tie1"  ,1   )
    self.cPutPortInVector( self.df_port[ "Tie-0 Port" ]  ,"tie0"  ,0   )
    self.cPutPortInVector( self.df_port[ "Tie-X Port" ]  ,"tiex"  ,'x' )
    if ( self.args.ifi2c ):
        self.cPutPortInVector( self.df_port[ "I2C-SCL" ] ,"i2c-scl", 1 )
        self.cPutPortInVector( self.df_port[ "I2C-SDA" ] ,"i2c-sda", 1 )
    elif ( self.args.ifspi ):
        self.cPutPortInVector( self.df_port[ "SPI-SS"  ] ,"spi-ss" , 1 )
        self.cPutPortInVector( self.df_port[ "SPI-CLK" ] ,"spi-clk", 0 )
        self.cPutPortInVector( self.df_port[ "SPI-DI"  ] ,"spi-di" , 1 )
        self.cPutPortInVector( self.df_port[ "SPI-DO"  ] ,"spi-do" , 0 )
    #----------Parse Port Data---------------------------------------------
    for p in self.vector:
        print("Port: %18s, Protocol = %10s, Value = %3s " % ( p.name, p.protocol, str(p.value) ) )
#----------------------------------------------------------------------------
def _GenVectorList( self ):
    result = ""
    for p in self.vector:
        result += p.name
        if p != self.vector[-1]:
            result += ", "
    return result
#----------------------------------------------------------------------------
def _GenATP_Idle( self, cnt ):
    #Reset
    for p in self.vector:
        if p.protocol == "tie1":     p.value = 1
        if p.protocol == "tie0":     p.value = 0
        if p.protocol == "tiex":     p.value = "x"
        if p.protocol == "spi-ss":   p.value = 1
        if p.protocol == "spi-clk":  p.value = 0
        if p.protocol == "spi-di":   p.value = 0
        if p.protocol == "spi-do":   p.value = 0
        if p.protocol == "i2c-scl":  p.value = 1
        if p.protocol == "i2c-sda":  p.value = 1
    self.f.write("//Begin being at Idle !\n")
    for i in range(0,cnt):
        self.cGenATPbyValue()
#----------------------------------------------------------------------------
def _GenATP( self ):
    self.f = open( self.args.outfname, "w" )
    self.f.write( "import tset frcgen0;\n" )
    self.f.write( "vector \t( $tset, %s ) \n" % self.cGenVectorList() )
    self.f.write( "{\n" )
    self.f.write( "burst_start_0:\n" )
    self.cGenATP_Idle(10)
    #-----------Instruction from Excel---------------------------------------
    row_cnt = self.df_cmd.shape[0]
    for i in range( 0, row_cnt ):
        cmd = self.df_cmd.iloc[i]
        if self.args.ifi2c: 
            self.cSet_I2C_Format( cmd )
        elif self.args.ifspi:
            self.cSet_SPI_Format( cmd )

    self.f.write( "}\n" )
    self.f.close()
#----------------------------------------------------------------------------
def _Set_SPI_SS_CLK_DI_DO( self, a, b, c, d ):
    for p in self.vector:
        if p.protocol == "spi-ss":
            p.value = a
        if p.protocol == "spi-clk":
            p.value = b
        if p.protocol == "spi-di":
            p.value = c
        if p.protocol == "spi-do":
            p.value = d
    self.cGenATPbyValue()
#----------------------------------------------------------------------------
def _Set_SPI_Reg_Addr( self, cmd ):
    self.f.write("//(SPI) Begin writing 24-bit Reg Address\n")
    self.f.write("//(SPI) Address = %s \n" % cmd.Address )
    adrr = bin(int(cmd.Address,16))[2:].zfill(24)[::-1]
    adrr = adrr[16:24][::-1] + adrr[8:16][::-1] + adrr[0:8][::-1]
    for b in adrr:
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, b, 0 )       
    self.f.write("//(SPI) End writing 24-bit Reg Address\n")
#----------------------------------------------------------------------------
def _Set_SPI_RW_Data( self, cmd ):
    rw = cmd.Command
    self.f.write("//(SPI) Begin %s data\n" % rw)
    self.f.write("//(SPI) Data = %s \n" % cmd.Value )
    value = cmd.Value.replace( "_", "" ).zfill(32)[::-1]
    value = value[24:32][::-1] + value[16:24][::-1] + value[8:16][::-1] + value[0:8][::-1]
    for v in value:
        if rw == "read":
            if v == "1":
                v = "H"
            elif v == "0":
                v = "L"
            self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, v )
        else:
            self.cSet_SPI_SS_CLK_DI_DO( 0, 0, v, 0 )
    self.f.write("//(SPI) End %s data\n" % rw)
#----------------------------------------------------------------------------
def _Set_SPI_Format( self, cmd ):
    if (cmd.Protocol != "SPI") or (cmd.Command != "read" and cmd.Command != 'write') or (not self.args.ifspi):
        return
    else:
        self.cGenATP_Idle(10)
        #------OP-Write-----------------------
        self.f.write("//(SPI) Start! SPI_CSI 1 -> 0 \n")
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.f.write("//(SPI) Start writing OP code\n")
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 1, 0 )
        if cmd.Command == "read":
            self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 1, 0 )
            self.f.write("//(SPI) End writing OP code for Read 8'h03\n")
        else:
            self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
            self.f.write("//(SPI) End writing OP code for Read 8'h02\n")
        #------Write 24 bits Address-----------
        self.cSet_SPI_Reg_Addr( cmd )
        #------RW Data-------------------------
        self.cSet_SPI_RW_Data( cmd )
#----------------------------------------------------------------------------
def _Set_I2C_SCL_SDA( self, SCL, SDA ):
    for p in self.vector:
        if p.protocol == "i2c-scl":
            p.value = SCL
        if p.protocol == "i2c-sda":
            p.value = SDA
    self.cGenATPbyValue()
#----------------------------------------------------------------------------
def _Set_I2C_Ctrl_Byte( self, ctrl_byte ):
    self.f.write("//(I2C) Begin writing ctrl bytes\n")
    for ctrl in ctrl_byte:
        self.cSet_I2C_SCL_SDA( 0, ctrl )
    self.cSet_I2C_SCL_SDA( 0, 0   ) #R/W, Write
    self.cSet_I2C_SCL_SDA( 0, "L" )#--ACK from DUT
    self.f.write("//(I2C) End writing ctrl bytes\n")
#----------------------------------------------------------------------------
def _Set_I2C_Reg_Addr( self, cmd ):
    self.f.write("//(I2C) Begin writing 24-bit Reg Address\n")
    self.f.write("//(I2C) Address = %s \n" % cmd.Address )
    adrr = bin(int(cmd.Address,16))[2:].zfill(24)[::-1]
    adrr = adrr[0:8][::-1] + adrr[8:16][::-1] + adrr[16:24][::-1]
    ctr  = 1
    for b in adrr:
        self.cSet_I2C_SCL_SDA( 0, b )
        if ctr == 8:
            ctr = 1
            self.cSet_I2C_SCL_SDA( 0, "L" )#Ack from slave
            self.f.write("//(I2C) ACK from slave to master, due to one byte/8 bits\n")
        else:
            ctr += 1
    self.f.write("//(I2C) End writing 24-bit Reg Address\n")
#----------------------------------------------------------------------------
def _Set_I2C_RW_Data( self, cmd ):
    rw = cmd.Command
    ack= 0 if cmd.Command == "read" else "L"
    self.f.write("//(I2C) Begin %s data\n" % rw)
    self.f.write("//(I2C) Data = %s \n" % cmd.Value )
    value = cmd.Value.replace( "_", "" ).zfill(32)[::-1]
    value = value[0:8][::-1] + value[8:16][::-1] + value[16:24][::-1] + value[24:32][::-1]
    ctr   = 1
    byte  = 1
    for v in value:
        if rw == "read":
            if v == "1":
                v = "H"
            elif v == "0":
                v = "L"

        self.cSet_I2C_SCL_SDA( 0, v )
        if ctr == 8:
            ctr = 1
            self.cSet_I2C_SCL_SDA( 0, ack )#Ack from master to slave
            self.f.write("//(I2C) ACK from master to slave, due to one byte/8 bits\n")
            byte += 1
        else:
            ctr += 1
    self.f.write("//(I2C) End %s data\n" % rw)
#----------------------------------------------------------------------------
def _Set_I2C_Start( self ):
    self.f.write("//I2C Start\n")
    self.cSet_I2C_SCL_SDA( 1, 1 )
    self.cSet_I2C_SCL_SDA( 1, 1 )
    self.cSet_I2C_SCL_SDA( 1, 1 )
    self.cSet_I2C_SCL_SDA( 1, 0 )
#----------------------------------------------------------------------------
def _Set_I2C_End( self ):
    self.f.write("//I2C End\n")
    self.cSet_I2C_SCL_SDA( 0, 0 )
    self.cSet_I2C_SCL_SDA( 1, 1 )
    self.cSet_I2C_SCL_SDA( 1, 1 )
    self.cSet_I2C_SCL_SDA( 1, 1 )
    self.cSet_I2C_SCL_SDA( 1, 1 )
    self.cSet_I2C_SCL_SDA( 1, 1 )
#----------------------------------------------------------------------------
def _Set_I2C_Format( self, cmd ):
    if (cmd.Protocol != "I2C") or (cmd.Command != "read" and cmd.Command != "write") or (not self.args.ifi2c):
        return
    else:
        ctrl = self.args.ctrlbyte #Ctrl byte
        #--Start------------------
        self.cSet_I2C_Start()
        #--Ctrl byte-------------- 
        self.cSet_I2C_Ctrl_Byte( ctrl )
        #--Write Reg Addr---------
        self.cSet_I2C_Reg_Addr( cmd )
        if cmd.Command == "read":
            #--Set Start--------------
            self.cSet_I2C_SCL_SDA( 0, 1 )
            self.cSet_I2C_SCL_SDA( 1, 0 )
            #--Ctrl byte-------------- 
            self.cSet_I2C_Ctrl_Byte( ctrl )
        #--RW Data-------------
        self.cSet_I2C_RW_Data( cmd )
        #--End---------------------
        self.cSet_I2C_End()
#----------------------------------------------------------------------------
def _GenATPbyValue( self ):
    vtr = ">frcgen0 "
    for p in self.vector:
        vtr += str(p.value) + " "
    self.f.write( "%s;\n" % vtr )  
#----------------------------------------------------------------------------
if __name__ == '__main__':
    myconvt = converter()
    myconvt.cParseArgs()
    myconvt.cParseDataFame()
    myconvt.cGenATP()
    
