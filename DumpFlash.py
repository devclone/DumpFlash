import sys
import pprint

class Flash:
	parity = ( 
		0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0,
		1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1,
		1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1,
		0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0,
		1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1,
		0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0,
		0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0,
		1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1,
		1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1,
		0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0,
		0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0,
		1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1,
		0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0,
		1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1,
		1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1,
		0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0
	)
			
	DebugLevel=0
	PageSize=0x200
	OOBSize=0x10
	PageCountPerBlock=0x20
	def __init__(self):
		self.BlockSize = (self.PageSize+self.OOBSize) * self.PageCountPerBlock

	def Open(self,filename):
		try:
			self.fd=open(filename,'rb')
		except:
			return False
		return True

	def Close(self):
		self.fd.close()
	
	def CalcECC(self, body):
		p8 = 0
		p8_ = 0
		p16 = 0
		p16_ = 0
		p32 = 0
		p32_ = 0
		p64 = 0
		p64_ = 0
		p128 = 0
		p128_ = 0
		p256 = 0
		p256_ = 0
		p512 = 0
		p512_ = 0
		p1024 = 0
		p1024_ = 0
		p2048 = 0
		p2048_ = 0
	
		p1 = 0
		p1_ = 0
		p2 = 0
		p2_ = 0
		p4 = 0
		p4_ = 0
	
		for i in range(0,len(body),1):
			ch=ord(body[i])
			bit0 = ch & 0x1
			bit1 = (ch >> 1) & 0x1
			bit2 = (ch >> 2) & 0x1
			bit3 = (ch >> 3) & 0x1
			bit4 = (ch >> 4) & 0x1
			bit5 = (ch >> 5) & 0x1
			bit6 = (ch >> 6) & 0x1
			bit7 = (ch >> 7) & 0x1
	
			xor_bit = bit7 ^ bit6 ^ bit5 ^ bit4 ^ bit3 ^ bit2 ^ bit1 ^ bit0

			if self.DebugLevel>0:
				print "%3x  " % i, bit7, bit6, bit5, bit4, bit3, bit2, bit1, bit0
	
			if i & 0x01 == 0x01:
				p8 = xor_bit ^ p8
			else:
				p8_ = xor_bit ^ p8_
	
			if i & 0x02 == 0x02:
				p16 = xor_bit ^ p16
			else:
				p16_ = xor_bit ^ p16_
	
			if i & 0x04 == 0x04:
				p32 = xor_bit ^ p32
			else:
				p32_ = xor_bit ^ p32_
	
			if i & 0x08 == 0x08:
				p64 = xor_bit ^ p64
			else:
				p64_ = xor_bit ^ p64_
	
			if i & 0x10 == 0x10:
				p128 = xor_bit ^ p128
			else:
				p128_ = xor_bit ^ p128_
	
			if i & 0x20 == 0x20:
				p256 = xor_bit ^ p256
			else:
				p256_ = xor_bit ^ p256_
	
			if i & 0x40 == 0x40:
				p512 = xor_bit ^ p512
			else:
				p512_ = xor_bit ^ p512_
			
			if i & 0x80 == 0x80:
				p1024 = xor_bit ^ p1024
			else:
				p1024_ = xor_bit ^ p1024_
	
			if i & 0x100 == 0x100:
				p2048 = xor_bit ^ p2048
			else:
				p2048_ = xor_bit ^ p2048_
	
			p1 = bit7 ^ bit5 ^ bit3 ^ bit1 ^ p1
			p1_ = bit6 ^ bit4 ^ bit2 ^ bit0 ^ p1_
			p2 = bit7 ^ bit6 ^ bit3 ^ bit2 ^ p2
			p2_ = bit5 ^ bit4 ^ bit1 ^ bit0 ^ p2_
			p4 = bit7 ^ bit6 ^ bit5 ^ bit4 ^ p4
			p4_ = bit3 ^ bit2 ^ bit1 ^ bit0 ^ p4_
	
		ecc0 = (p64 << 7) + (p64_ << 6) + (p32 << 5) + (p32_ << 4) + (p16 << 3) + (p16_ << 2) + (p8 << 1) + ( p8_ << 0)
		ecc1 = (p1024 << 7) + (p1024_ << 6) + (p512 << 5) + (p512_ << 4) + (p256 << 3) + (p256_ << 2) + (p128 << 1) + (p128_<< 0)
		ecc2 = (p4 << 7) + (p4_ << 6) + (p2 << 5) + (p2_ << 4) + (p1 << 3) + (p1_ << 2) + (p2048 << 1) + (p2048_ << 0)
	
		return ( ecc0 ^ 0xff, ecc1 ^ 0xff, ecc2 ^ 0xff)

	def CalcECC2(self, body):
		par = 0
		rp0 = 0
		rp1 = 0
		rp2 = 0
		rp3 = 0
		
		rp4 = 0
		rp5 = 0
		rp6 = 0
		rp7 = 0
		
		rp8 = 0
		rp9 = 0
		rp10 = 0
		rp11 = 0
		
		rp12 = 0
		rp13 = 0
		rp14 = 0
		rp15 = 0
	
		for i in range(0,len(body),1):
			cur = ord(body[i])
			par ^= cur
	
			if i & 0x01:
				rp1 ^= cur
			else:
				rp0 ^= cur
			
			if i & 0x02:
				rp3 ^= cur
			else:
				rp2 ^= cur
	
			if i & 0x04:
				rp5 ^= cur
			else:
				rp4 ^= cur
		
			if i & 0x08:
				rp7 ^= cur
			else:
				rp6 ^= cur
	
			if i & 0x10:
				rp9 ^= cur
			else:
				rp8 ^= cur
	
			if i & 0x20:
				rp11 ^= cur
			else:
				rp10 ^= cur
	
			if i & 0x40:
				rp13 ^= cur
			else:
				rp12 ^= cur
	
			if i & 0x80:
				rp15 ^= cur
			else:
				rp14 ^= cur
	
		code0 = \
			( self.Parity[rp7] << 7 ) | \
			( self.Parity[rp6] << 6 ) | \
			( self.Parity[rp5] << 5 ) | \
			( self.Parity[rp4] << 4 ) | \
			( self.Parity[rp3] << 3 ) | \
			( self.Parity[rp2] << 2 ) | \
			( self.Parity[rp1] << 1 ) | \
			( self.Parity[rp0] << 0 ) 
	
		code1 = \
			( self.Parity[rp15] << 7 ) | \
			( self.Parity[rp14] << 6 ) | \
			( self.Parity[rp13] << 5 ) | \
			( self.Parity[rp12] << 4 ) | \
			( self.Parity[rp11] << 3 ) | \
			( self.Parity[rp10] << 2 ) | \
			( self.Parity[rp9] << 1 ) | \
			( self.Parity[rp8] << 0 ) 
	
		code2 = \
			( self.Parity[par & 0xf0] << 7 ) | \
			( self.Parity[par & 0x0f] << 6 ) | \
			( self.Parity[par & 0xcc] << 5 ) | \
			( self.Parity[par & 0x33] << 4 ) | \
			( self.Parity[par & 0xaa] << 3 ) | \
			( self.Parity[par & 0x55] << 2 ) 
	
		code0 = ~code0
		code1 = ~code1
		code2 = ~code2
	
		return (code0,code1,code2)

	def CheckECC(self):
		block = 0
		end_of_file=False
		count=0
		error_count=0

		while 1:
			for page in range(0,self.PageCountPerBlock,1):
				offset = (block * (self.PageSize+self.OOBSize) * self.PageCountPerBlock) + page * (self.PageSize+self.OOBSize)
				self.fd.seek(offset,0)
				data = self.fd.read(self.PageSize+self.OOBSize)
				
				if not data:
					end_of_file=True
					break
	
				count+=1
				body = data[0:self.PageSize]
				ecc0_ = ord(data[self.PageSize])
				ecc1_ = ord(data[513])
				ecc2_ = ord(data[514])
		
				if ecc0_==0xff and ecc1_==0xff and ecc2_==0xff:
					continue
		
				( ecc0, ecc1, ecc2) = self.CalcECC(body)
		
				ecc0_xor = ecc0 ^ ecc0_
				ecc1_xor = ecc1 ^ ecc1_
				ecc2_xor = ecc2 ^ ecc2_
		
				if ecc0_xor != 0 or ecc1_xor != 0 or ecc2_xor != 0:
					error_count+=1
					print "Checksum error block: %d page: %d at 0x%x" % (block, page, offset)
					print "Orig: 0x%2x 0x%2x 0x%2x" % ( ecc0_, ecc1_, ecc2_)
					print "Calc: 0x%2x 0x%2x 0x%2x" % ( ecc0, ecc1, ecc2)
					print "XOR:  0x%2x 0x%2x 0x%2x" % ( ecc0 ^ ecc0_, ecc1 ^ ecc1_, ecc2 ^ ecc2_)
					print ''
		
			if end_of_file:
				break
		
			block += 1
	
		print "Checked %d ECC record and found %d errors" % (count,error_count)

	def IsBadBlockPage(self,oob,block_offset):
		bad_block=False
		if oob[0:3]!='\xff\xff\xff':
			bad_block=True

			if oob[0x8:]== '\x85\x19\x03\x20\x08\x00\x00\x00':
				self.fd.seek(block_offset)
				block_sig = self.fd.read(2)

				if block_sig=='\x85\x19':
					bad_block=False

		return bad_block

	CLEAN_BLOCK=0
	BAD_BLOCK=1
	ERROR=2

	def IsBadBlock(self,block):
		for page in range(0,2,1):
			block_offset = (block * self.BlockSize ) + (page * (self.PageSize + self.OOBSize))
			self.fd.seek( block_offset + self.PageSize+8 )
			bad_block_byte = self.fd.read(1)
	
			if not bad_block_byte:
				return self.ERROR

			if bad_block_byte != '\xff':
				self.fd.seek(block_offset+self.PageSize)
				oob = self.fd.read(self.OOBSize)
				if self.IsBadBlockPage(oob,block_offset):
					return self.BAD_BLOCK
		return self.CLEAN_BLOCK

	def CheckBadBlocks(self):
		block = 0
		end_of_file=False
		error_count=0

		while 1:
			ret=self.IsBadBlock(block)

			if ret==self.BAD_BLOCK:
				error_count+=1
				print "Checksum error block: %d (0x%x) page: %d at 0x%x" % (block, block_offset, page, offset)
				print "\t%s" % pprint.pformat(oob)
	
			elif ret==self.ERROR:
				break

			block += 1

		print "Checked %d blocks and found %d errors" % (block,error_count)
	
	def Extract(self, output_filename, start, size):
		end = start + size
		wfd=open(output_filename,"wb")

		start_block = ( start / self.BlockSize )
		end_block = ( end / self.BlockSize )

		print 'Dumping blocks (%d - %d)' % (start_block, end_block)

		for block in range(start_block,end_block,1):
			ret=self.IsBadBlock(block)

			if ret==self.CLEAN_BLOCK:
				for page in range(0,self.PageCountPerBlock,1):
					self.fd.seek( block * self.BlockSize + page * (self.PageSize+self.OOBSize) )
					data = self.fd.read(self.PageSize)
					oob = data[self.PageSize:]
					wfd.write(data[0:self.PageSize])

			elif ret==self.ERROR:
				break
		
		wfd.close()

if __name__=='__main__':
	from optparse import OptionParser

	parser = OptionParser()
	parser.add_option("-o", "--output", dest="output",
                  help="Output filename", metavar="OUTPUT")

	parser.add_option("-b", action="store_true", dest="check_bad_blocks")
	parser.add_option("-e", action="store_true", dest="check_ecc")
	parser.add_option("-r", type="int", nargs=2, dest="range")

	(options, args) = parser.parse_args()

	filename = args[0]

	print 'Opening', filename

	flash = Flash()

	if flash.Open(filename):
		if options.check_bad_blocks:
			print 'Check bad blocks:'
			flash.CheckBadBlocks()
	
		if options.check_ecc:
			print 'Check ECC:'
			flash.CheckECC()
	
		if options.range!=None and options.output!=None:
			print 'Extract range(%x - %x) to %s' % ( options.range[0], options.range[1], options.output)
			flash.Extract(options.output,  options.range[0], options.range[1])

		flash.Close()

