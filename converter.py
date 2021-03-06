#--------------------------------------------------------------------
#  Import API
#--------------------------------------------------------------------
import os
import pandas   as pd
import argparse as ag
import time     as t
#---------------------------------------------------------------------
class Port:
    def __init__( self, name, value ):
        self.name     = name
        self.value    = value
        self.protocol = ""
        self.ini_value= value
#---------------------------------------------------------------------
class converter:
    def __init__( self ):
        self.args        = ''
        self.unknown     = ''
        self.input       = ''
        self.df_port     = ''
        self.df_cmd      = ''
        self.vector      = []
        self.f           = ''
        self.excel       = ''
        self.cmd_list    = [ "W", "R", "R", "RH", "RL", "D", "F" ]
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
    def cSet_I2C_Ctrl_Byte( self, ctrl, rw ):
        _Set_I2C_Ctrl_Byte( self, ctrl, rw )
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
     #-----SMI(MDC/MDIO)---------------------------
    def cSet_SMI_Format( self, cmd ):
        _Set_SMI_Format( self, cmd )
    def cSet_SMI_MDC_MDIO( self, a, b ):
        _Set_SMI_MDC_MDIO( self, a, b )
    def cSet_SMI_Phy_Addr( self, cmd ):
        _Set_SMI_Phy_Addr( self, cmd )
    def cSet_SMI_Reg_Addr( self, cmd ):
        _Set_SMI_Reg_Addr( self, cmd )
    def cSet_SMI_RW_Data( self, cmd ):
        _Set_SMI_RW_Data( self, cmd )
    #----Basic--------------------------------------
    def cGenATPbyValue( self ):
        _GenATPbyValue( self  )
#----------------------------------------------------------------------------
def _ParseArgs( self ):
    print( t.asctime( t.localtime( t.time() ) ) )
    example = "\
    Example: \n\
    (linux, macOS)        ./converter.py -input i2c_pattern.xlsx -output i2c_pattern.atp -i2c \n\
    (   Windows  ) python .\converter.py -input i2c_pattern.xlsx -output i2c_pattern.atp -i2c \n\
    "

    help_in    = "Your excel input"
    help_spi   = "Convert the SPI to ATP based on SPI protocol"
    help_i2c   = "Convert the I2C to ATP based on I2C protocol"
    help_smi   = "Convert the MDIO/MDC to ATP based on smi protocol"
    help_out   = "Specify your output ATP filename"
    help_ctrl  = "Specify your I2c ctrl byte, 1010100 at default."
    help_dummy = "Specify your SPI dummy cycle"
    parser     = ag.ArgumentParser( epilog=example, formatter_class=ag.RawTextHelpFormatter )
    parser.add_argument( "-input"               ,help=help_in        ,dest="infname"            ,default="" )
    parser.add_argument( "-spi"                 ,help=help_spi       ,dest="ifspi"              ,default=False          ,action="store_true")
    parser.add_argument( "-i2c"                 ,help=help_i2c       ,dest="ifi2c"              ,default=False          ,action="store_true")
    parser.add_argument( "-smi"                 ,help=help_smi       ,dest="ifsmi"              ,default=False          ,action="store_true")
    parser.add_argument( "-spi_ctrlbyte"        ,help=help_ctrl      ,dest="ctrlbyte"           ,default="1010100")
    parser.add_argument( "-spi_dummy"           ,help=help_dummy     ,dest="dumycycle"          ,default=8              ,type=int)
    parser.add_argument( "-smi_phy_adr"         ,help=help_dummy     ,dest="phy_adr"            ,default="0x18")
    self.args, self.unknown = parser.parse_known_args()
    #----------------Checker------------------------------------------
    if ( self.args.infname == "" ):
        print( "[Error] Your input excel file is not specify by arg -input" )
        exit(-1)
    if ( not self.args.ifi2c ) and ( not self.args.ifspi ) and ( not self.args.ifsmi ):
        print( "[Error] One of args \"-spi\" ,\"-i2c\" or \"-smi\" must be specidfied" )
        exit(-1)
    if ( self.args.ifi2c ) and ( self.args.ifspi ) and ( self.args.ifsmi ):
        print( "[Error] Only one of args \"-spi\" , \"-i2c\" \"-smi\" can be specidfied" )
        exit(-1)
    #-------------------------------------------------------------------
    print( "[Setting] Input     : %s"    % self.args.infname )
    print( "[Setting] I2C -> ATP:" , self.args.ifi2c)
    print( "[Setting] SPI -> ATP:" , self.args.ifspi )
    print( "[Setting] SMI -> ATP:" , self.args.ifsmi )
#----------------------------------------------------------------------------
def _PutPortInVector( self, port_list, protocol, value ):
    for p in port_list:
        if ( not pd.isna(p) ):
            p_inst = Port( p, value )
            if ( p_inst not in self.vector ):
                p_inst.protocol = protocol
                self.vector.append( p_inst )
            else:
                print( "[Error] Port %s is duplicated" )
#----------------------------------------------------------------------------
def _ParseDataFrame( self ):
    try:
        self.excel   = pd.ExcelFile( self.args.infname )
        print( "[Info] Reading %s" % self.args.infname )
    except:
        print( "[Error] Fail to read excel" )
        print( "[Error] Input file must be *.xlsx format. Maybe your input is *.csv or other formates, which is not allowed" )
    #----------Parse Port Data---------------------------------------------
    if(   "_start" not in self.excel.sheet_names ):
        print( "[Error] No \"_start\" sheet in your excel" )
        exit(-1)
    elif( "_end"   not in self.excel.sheet_names ):
        print( "[Error] No \"_end\" sheet in your excel" )
        exit(-1)
    elif( "PORT"   not in self.excel.sheet_names ):
        print( "[Error] No \"PORT\" sheet in your excel" )
        exit(-1)
    self.df_port = self.excel.parse("PORT")

    self.cPutPortInVector( self.df_port[ "Tie-1 Port" ]  ,"tie1"  , 1  )
    self.cPutPortInVector( self.df_port[ "Tie-0 Port" ]  ,"tie0"  , 0  )
    self.cPutPortInVector( self.df_port[ "Tie-X Port" ]  ,"tiex"  ,'x' )
    if ( self.args.ifi2c ):
        self.cPutPortInVector( self.df_port[ "I2C-SCL" ] ,"i2c-scl", 1 )
        self.cPutPortInVector( self.df_port[ "I2C-SDA" ] ,"i2c-sda", 1 )
    elif ( self.args.ifspi ):
        self.cPutPortInVector( self.df_port[ "SPI-SS"  ] ,"spi-ss" , 1 )
        self.cPutPortInVector( self.df_port[ "SPI-CLK" ] ,"spi-clk", 1 )
        self.cPutPortInVector( self.df_port[ "SPI-DI"  ] ,"spi-di" , 0 )
        self.cPutPortInVector( self.df_port[ "SPI-DO"  ] ,"spi-do" , 0 )
    elif (self.args.ifsmi ):
        self.cPutPortInVector( self.df_port[ "SMI-MDC" ] ,"smi-mdc"  , 1 )
        self.cPutPortInVector( self.df_port[ "SMI-MDIO"] ,"smi-mdio" , 1 )
    #----------Parse Port Data---------------------------------------------
    print( "[Info] The result parsed from xlsx is concluded below" )
    for p in self.vector:
        print("\tPort: %16s, Protocol = %10s, Value = %3s " % ( p.name, p.protocol, str(p.value) ) )
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
        p.value = p.ini_value
        
    self.f.write("//Begin being at Idle !\n")
    for i in range(0,cnt):
        self.cGenATPbyValue()
#----------------------------------------------------------------------------
def check_CMD( cmd ):
    result = True
    if( type(cmd.REGISTER) != str ):
        print("[Error] The reg addr must be present in string format")
        result = False
    elif( type(cmd.DATA) != str ):
        print("[Error] The reg value must be present in string format")
        result = False
    elif( "0x" not in cmd.REGISTER ):
        print("[Error] The reg addr must be present in hex, e.g., 0x...")
        result = False
    else:
        result = True
    if (not result):
        print("[Error] The folowing cmd cause error:")
        print( cmd )
    return result
#----------------------------------------------------------------------------
def _GenATP( self ):
    sheet_list = []
    meet_start = False
    for sheet in self.excel.sheet_names:
        if  ( sheet == "_start" ):
            meet_start = True
            continue
        elif( sheet == "_end"   ):
            break
        if( meet_start ):
            sheet_list.append( sheet )

    if( len(sheet_list) == 0 ):
        print("[ERROR] No sheet is available. Maybe _start or _end sheet is placed in wrong order")
        exit(-1)

    for sheet_name in sheet_list:
       self.f = open( sheet_name + ".atp" , "w" )
       self.f.write( "import tset frcgen0;\n" )
       self.f.write( "vector \t( $tset, %s ) \n" % self.cGenVectorList() )
       self.f.write( "{\n" )
       self.f.write( "burst_start_0:\n" )
       self.cGenATP_Idle(10)
    #-----------Instruction from Excel---------------------------------------
       self.df_cmd = self.excel.parse( sheet_name )
       row_cnt = self.df_cmd.shape[0]
       for i in range( 0, row_cnt ):
           cmd = self.df_cmd.iloc[i]
           
           #Check cmd format in xlsx
           cmd.DATA = str( cmd.DATA )
           if( cmd.COMMAND == "D" ):
               self.cGenATP_Idle( int( cmd.DATA ) )
               continue
           elif( not check_CMD( cmd ) ):
               exit(-1)


           if(   self.args.ifi2c ): 
               self.cSet_I2C_Format( cmd )
           elif( self.args.ifspi ):
               self.cSet_SPI_Format( cmd )
           elif( self.args.ifsmi ):
               self.cSet_SMI_Format( cmd )

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
    #The address must be present in hex format
    self.f.write("//(SPI) Begin writing 24-bit Reg Address\n")
    self.f.write("//(SPI) Address = %s \n" % cmd.REGISTER )
    adrr = bin(int(cmd.REGISTER,16))[2:].zfill(24)[::-1]
    adrr = adrr[16:24][::-1] + adrr[8:16][::-1] + adrr[0:8][::-1]
    for b in adrr:
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, b, 0 )       
    self.f.write("//(SPI) End writing 24-bit Reg Address\n")
#----------------------------------------------------------------------------
def isDataBinary( DATA ):
    assert type( DATA ) == str, "DATA should be present in string format"
    length = len( DATA.replace( "_", "" ) )
    
    if  ( DATA[0:2] != "0x" ) and ( DATA[0:2] != "0X"):
        return True
    elif( "_" in DATA ):
        return True
    elif( length == 16 ) or ( length == 32 ):
        return True
    else:
        return False #Hex
#----------------------------------------------------------------------------
def _Set_SPI_RW_Data( self, cmd ):
    rw = cmd.COMMAND
    self.f.write("//(SPI) Begin %s data\n" % rw)
    self.f.write("//(SPI) Data = %s \n" % cmd.DATA )
    value = 0
    #Hex format (Must be 32 bit)
    if not isDataBinary( cmd.DATA ):
        if( "W" in cmd.COMMAND ):
            value =  bin(int(cmd.DATA,16))[2:].zfill(32)[::-1]
        else:
            value =  bin(int(cmd.DATA,16))[2:].rjust(32,"x")[::-1]
    #Binary format
    else:
        if( "W" in cmd.COMMAND ):
            value = cmd.DATA.replace( "_", "" ).zfill(32)[::-1]
        else:#R, RL, RH
            value = cmd.DATA.replace( "_", "" ).rjust(32,"x")[::-1]
       
    value = value[24:32][::-1] + value[16:24][::-1] + value[8:16][::-1] + value[0:8][::-1]
    for v in value:
        if "R" in rw :
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
    if ( cmd.COMMAND not in self.cmd_list ) or (not self.args.ifspi):
        return
    else:
        self.cGenATP_Idle(10)
        #------OP-Write-----------------------
        self.f.write("//(SPI) Start! SPI_CSI 1 -> 0 \n")
        self.f.write("//(SPI) Start writing OP code\n")
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
        self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 1, 0 )
        if ( cmd.COMMAND == "R" ) or ( cmd.COMMAND == "RH" ) or ( cmd.COMMAND == "RL" ) :
            self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 1, 0 )
            self.f.write("//(SPI) End writing OP code for Read 8'h03\n")
        else:
            self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
            self.f.write("//(SPI) End writing OP code for Read 8'h02\n")
        #------Write 24 bits Address-----------
        self.cSet_SPI_Reg_Addr( cmd )
        #------Dummy if Read-------------------
        if ( cmd.COMMAND == "R" ) or ( cmd.COMMAND == "RH" ) or ( cmd.COMMAND == "RL" ) :
            self.f.write("//(SPI) Begin Dummy\n")
            for i in range( self.args.dumycycle ):
                self.cSet_SPI_SS_CLK_DI_DO( 0, 0, 0, 0 )
            self.f.write("//(SPI) End Dummy\n")
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
def _Set_I2C_Ctrl_Byte( self, ctrl_byte, rw ):
    self.f.write("//(I2C) Begin writing ctrl bytes\n")
    rwb = 0 if (rw == "w") else 1
    for ctrl in ctrl_byte:
        self.cSet_I2C_SCL_SDA( 0, ctrl )
    self.cSet_I2C_SCL_SDA( 0, rwb   ) #R/W, Write
    self.cSet_I2C_SCL_SDA( 0, "L" )#--ACK from DUT
    self.f.write("//(I2C) End writing ctrl bytes\n")
#----------------------------------------------------------------------------
def _Set_I2C_Reg_Addr( self, cmd ):
    self.f.write("//(I2C) Begin writing 24-bit Reg Address\n")
    self.f.write("//(I2C) Address = %s \n" % cmd.REGISTER )
    adrr = bin(int(cmd.REGISTER,16))[2:].zfill(24)[::-1]
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
    rw = cmd.COMMAND
    ack= 1 if ( "R" in cmd.COMMAND ) else "L"
    self.f.write("//(I2C) Begin %s data\n" % rw)
    self.f.write("//(I2C) Data = %s \n" % cmd.DATA )
    value = 0
    #Hex format (Must be 32 bit)
    if not isDataBinary( cmd.DATA ):
        if( "W" in cmd.COMMAND ):
            value =  bin(int(cmd.DATA,16))[2:].zfill(32)[::-1]
        else:
            value =  bin(int(cmd.DATA,16))[2:].rjust(32,"x")[::-1]
    #Binary format
    else:
        if( "W" in cmd.COMMAND ):
            value = cmd.DATA.replace( "_", "" ).zfill(32)[::-1]
        else:#R, RL, RH
            value = cmd.DATA.replace( "_", "" ).rjust(32,"x")[::-1]

    value = value[0:8][::-1] + value[8:16][::-1] + value[16:24][::-1] + value[24:32][::-1]
    ctr   = 1
    byte  = 1
    for v in value:
        if "R" in rw:
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
    self.cSet_I2C_SCL_SDA( 1, 0 )
#----------------------------------------------------------------------------
def _Set_I2C_End( self ):
    self.f.write("//I2C End\n")
    self.cSet_I2C_SCL_SDA( 0, 0 )
    self.cSet_I2C_SCL_SDA( 1, 1 )
    self.cSet_I2C_SCL_SDA( 1, 1 )
    self.cSet_I2C_SCL_SDA( 1, 1 )
#----------------------------------------------------------------------------
def _Set_I2C_Format( self, cmd ):
    if ( cmd.COMMAND not in self.cmd_list ) or ( not self.args.ifi2c ):
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
#----------------------------------------------------------------------------
def _GenATPbyValue( self ):
    vtr = ">frcgen0 "
    for p in self.vector:
        vtr += str(p.value) + " "
    self.f.write( "%s;\n" % vtr )  
#----------------------------------------------------------------------------
def _Set_SMI_MDC_MDIO( self, a, b ):
    for p in self.vector:
        if p.protocol == "smi-mdc":
            p.value = a
        if p.protocol == "smi-mdio":
            p.value = b
    self.cGenATPbyValue()
#----------------------------------------------------------------------------
def _Set_SMI_Format( self, cmd ):
    if ( cmd.COMMAND not in self.cmd_list ) or ( not self.args.ifsmi ):
        return
    else:   
        #--Preamble------------------
        self.f.write("//(SMI) Begin writing Preamble\n")
        for i in range(0,32):
            self.cSet_SMI_MDC_MDIO( 0, 1 )
        self.f.write("//(SMI) Finish writing Preamble\n")
        #--Start-------------- 
        self.f.write("//(SMI) Start\n")
        self.cSet_SMI_MDC_MDIO( 0, 0 )
        self.cSet_SMI_MDC_MDIO( 0, 1 )
        #--OP-----------------
        self.f.write("//(SMI) Begin writing OP\n")
        if "R" in cmd.COMMAND:
            self.cSet_SMI_MDC_MDIO( 0, 1 )
            self.cSet_SMI_MDC_MDIO( 0, 0 )
        else:
            self.cSet_SMI_MDC_MDIO( 0, 0 )
            self.cSet_SMI_MDC_MDIO( 0, 1 )
        self.f.write("//(SMI) Finish writing OP\n")
        #--Write PHY Addr---------
        self.cSet_SMI_Phy_Addr( cmd )
        #--Write Reg Addr---------
        self.cSet_SMI_Reg_Addr( cmd )
        #--Turn Around------------
        self.f.write("//(SMI) Begin writing TA\n")
        if "R" in cmd.COMMAND:
            self.cSet_SMI_MDC_MDIO( 0, 0 )#High-Z
            self.cSet_SMI_MDC_MDIO( 0, 0 )
        else:
            self.cSet_SMI_MDC_MDIO( 0, 1 )
            self.cSet_SMI_MDC_MDIO( 0, 0 )
        self.f.write("//(SMI) Begin writing TA\n")
        #--RW Data----------------
        self.cSet_SMI_RW_Data( cmd )
        #--End---------------------
        self.cGenATP_Idle(10)
#----------------------------------------------------------------------------
def _Set_SMI_Reg_Addr( self, cmd ):
    self.f.write("//(SMI) Begin writing Reg Address\n")
    self.f.write("//(SMI) Reg Address = %s \n" % cmd.REGISTER )

    addr = bin( int(cmd.REGISTER,16) )[2:].zfill(5)

    for b in addr:
        self.cSet_SMI_MDC_MDIO( 0, b )
    self.f.write("//(SMI) Finish writing Reg Address\n")
#----------------------------------------------------------------------------
def _Set_SMI_Phy_Addr( self, cmd ):
    self.f.write("//(SMI) Begin writing PHY Address\n")
    self.f.write("//(SMI) PHY Address = %s \n" % self.args.phy_adr ) 

    addr = bin(int(self.args.phy_adr,16))[2:].zfill(5)
    if( len(addr) > 5 ):
        print( "[Error] The PHY Address Length for SMI is larger than 5 bits" )
    for b in addr:
        self.cSet_SMI_MDC_MDIO( 0, b )
    self.f.write("//(SMI) Finish writing PHY Reg Address\n")
#----------------------------------------------------------------------------
def _Set_SMI_RW_Data( self, cmd ):
    rw = cmd.COMMAND
    ack= 0 if ( "R" in cmd.COMMAND ) else "L"
    self.f.write("//(SMI) Begin %s data\n" % rw)
    self.f.write("//(SMI) Data = %s \n" % cmd.DATA )

    value = 0
    #Hex format (Must be 32 bit)
    
    if not isDataBinary( cmd.DATA ):
        if( "W" in cmd.COMMAND ):
            value =  bin(int(cmd.DATA,16))[2:].zfill(16)
        else:
            value =  bin(int(cmd.DATA,16))[2:].rjust(16,"x")
    #Binary format
    else:
        if( "W" in cmd.COMMAND ):
            value = cmd.DATA.replace( "_", "" ).zfill(16)
        else:#R, RL, RH
            value = cmd.DATA.replace( "_", "" ).rjust(16,"x")

    if( len(value) > 16 ):
        print( "[Warning] The SMI DATA Length for SMI is larger than 16 (It should be 16 bits, based on SPEC)" )
        print( "Your DATA is ", value )

    for v in value:
        if "R" in rw:
            if v == "1":
                v = "H"
            elif v == "0":
                v = "L"
        self.cSet_SMI_MDC_MDIO( 0, v )
    self.f.write("//(Finish) Finish %s data\n" % rw)
#----------------------------------------------------------------------------
if __name__ == '__main__':
    myconvt = converter()
    myconvt.cParseArgs()
    myconvt.cParseDataFame()
    myconvt.cGenATP()
    
