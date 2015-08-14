
import kiss

k = kiss.KISS(host='10.10.0.214', speed=115200, port=8001)
k.logger.LOG_LEVEL = "DEBUG"
k.start()  # inits the TNC, optionally passes KISS config flags.
# k.write("testing")
# k.read()
# k.write('KB3DFZ-5>APDW10,WIDE1-1,WIDE2-1:testing')
k.read()


