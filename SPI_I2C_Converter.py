#--------------------------------------------------------------------
#  Import API
#--------------------------------------------------------------------
import os
import pandas as pd
import argparse as ag
#---------------------------------------------------------------------
class converter:
    def __init__( self ):
        self.df          = ''
        self.args        = ''
        self.unknown     = ''

    def parseArgs( self ):
        _parseArgs( self )

    def parseDataFame( self):
        _parseDataFrame( self )

#---------------------------------------------------------------------
def _parseArgs( self ):
    example = "\
    Example: \n\
    The script is being developed.... \n\
    "

    help_in    = "Your excel input"
    help_spi   = "Convert the SPI to ATP based on SPI protocol"
    help_i2c   = "Convert the I2C to ATP based on I2C protocol"
    help_out   = "Specify your output ATP filename"
    parser     = ag.ArgumentParser( epilog=example, formatter_class=argparser.RawTextHelpFormatter )
    parser.add_argument( "-input"               ,help=help_in        ,dest="infname"            ,default="" )
    parser.add_argument( "-spi"                 ,help=help_spi       ,dest="ifspi"              ,default=False          ,action="store_true")
    parser.add_argument( "-i2c"                 ,help=help_i2c       ,dest="ifi2c"              ,default=False          ,action="store_true")

    self.args, self.unknown = parser.parse_known_args()
    #----------------Checker------------------------------------------
    if ( self.args.infname == "" ):
        print( "[Error] Your input excel file is not specify by arg -input" )
        exit(-1)
    if ( not self.args.ifi2c ) and ( not self.args.ifi2c ):
        print( "[Error] One of args \"-spi\" or \"-i2c\" must be specidfy" )
        exit(-1)
def _parseDataFrame( self ):
    pass

#---------------------------------------------------------------------
if __name__ == '__main__':
    myconvt = converter()
    myconvt.parseArgs()
    myconvt.parseDataFame()
    
