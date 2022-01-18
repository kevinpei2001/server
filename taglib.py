# !/usr/bin/env python
import sys
import time
import math
import zlib
import threading
from datetime import datetime, timedelta
from dateutil import tz
from types import *
try:
    from io import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3

# long integer removed in python 3
try:
    int(0)
except NameError:
    def long(x): return int(x)

UnixEpochTicks = int(621355968000000000)
TicksPerDay = int(864000000000)
TicksPerHour = int(36000000000)
TicksPerMinute = int(600000000)
TicksPerSecond = int(10000000)
TicksPerMillisecond = int(10000)
TicksPerMicrosecond = int(10)

from struct import pack, unpack

sys.path.append('gen-py')

from bcl.ttypes import *
from common.ttypes import *
from tag.ttypes import *

from thrift import Thrift
from thrift.transport import TTransport


def ticks_to_utc(ticks):
    return(datetime.utcfromtimestamp(int(math.floor((ticks - UnixEpochTicks) / TicksPerSecond))) + timedelta(microseconds=int(math.floor(((ticks - UnixEpochTicks) %  TicksPerSecond) / TicksPerMicrosecond))))


def time_to_ticks(value):
    # note mktime uses local time not utc time
    #python 2 mktime return long integer.  python 3 returns float (probably loses precision)
    return int(time.mktime(value.timetuple())) * TicksPerSecond + UnixEpochTicks + value.microsecond * TicksPerMicrosecond


# convert bc
def convertFromDateTime(value):
    try:
        if value == None:
            return datetime.min
        elif value.scale == TimeSpanScale.DAYS:
            return datetime.utcfromtimestamp(ticks_to_time(value.value * TicksPerDay))
        elif value.scale == TimeSpanScale.HOURS:
            return datetime.utcfromtimestamp(ticks_to_time(value.value * TicksPerHour))
        elif value.scale == TimeSpanScale.MINUTES:
            return datetime.utcfromtimestamp(ticks_to_time(value.value * TicksPerMinute))
        elif value.scale == TimeSpanScale.SECONDS:
            return datetime.utcfromtimestamp(ticks_to_time(value.value * TicksPerSecond))
        elif value.scale == TimeSpanScale.MILLISECONDS:
            return datetime.utcfromtimestamp(ticks_to_time(value.value * TicksPerMillisecond))
        elif value.scale == TimeSpanScale.TICKS:
            if value.value == 0: return datetime.min
            return datetime.utcfromtimestamp(ticks_to_time(value.value))
        elif value.scale == TimeSpanScale.MINMAX:
            return value.value > 0 and datetime.max or datetime.min
        return datetime.min
    except Exception as ex:
        print(('DateTime: %s %s'%(value.scale, value.value)))
        print(('Exception: %s' % (ex.message)))
        import traceback; traceback.print_exc(file=sys.stdout)

def toLocalTime(dt):
    if dt == datetime.min or dt == datetime.max: 
        return dt
    return dt.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())


def convertToDateTime(value):
    result = DateTime()
    if value: ticks = time_to_ticks(value)
    if not ticks:
        result.scale = TimeSpanScale.TICKS
        result.value = 0
    elif value == datetime.max:
        result.scale = TimeSpanScale.MINMAX
        result.value = 1
    elif value == datetime.min:
        result.scale = TimeSpanScale.MINMAX
        result.value = -1
    elif ticks % TicksPerMillisecond == 0:
        if ticks % TicksPerSecond == 0:
            if ticks % TicksPerMinute == 0:
                if ticks % TicksPerHour == 0:
                    if ticks % TicksPerDay == 0:
                        result.scale = TimeSpanScale.DAYS
                        result.value = ticks / TicksPerDay
                    else:
                        result.scale = TimeSpanScale.HOURS
                        result.value = ticks / TicksPerHour
                else:
                    result.scale = TimeSpanScale.MINUTES
                    result.value = ticks / TicksPerMinute
            else:
                result.scale = TimeSpanScale.SECONDS
                result.value = ticks / TicksPerSecond
        else:
            result.scale = TimeSpanScale.MILLISECONDS
            result.value = ticks / TicksPerMillisecond
    else:
        result.scale = TimeSpanScale.TICKS
        result.value = ticks
    return result


def convertFromTimeSpan(value):
    if value == None:
        return timedelta()
    elif value.scale == TimeSpanScale.DAYS:
        return timedelta(days=value.value)
    elif value.scale == TimeSpanScale.HOURS:
        return timedelta(hours=value.value)
    elif value.scale == TimeSpanScale.MINUTES:
        return timedelta(minutes=value.value)
    elif value.scale == TimeSpanScale.SECONDS:
        return timedelta(seconds=value.value)
    elif value.scale == TimeSpanScale.MILLISECONDS:
        return timedelta(milliseconds=value.value)
    elif value.scale == TimeSpanScale.TICKS:
        return timedelta(microseconds=value.value / TicksPerMicrosecond)
    elif value.scale == TimeSpanScale.MINMAX:
        return value.value > 0 and timedelta.max or timedelta.min
    return datetime.min


def convertToTimeSpan(value):
    result = TimeSpan()
    if value: ticks = int(value.microseconds) * TicksPerMicrosecond + int(value.seconds) * TicksPerSecond + int(value.days) * TicksPerDay
    if not ticks:
        result.scale = TimeSpanScale.TICKS
        result.value = 0
    elif value == timedelta.max:
        result.scale = TimeSpanScale.MINMAX
        result.value = 1
    elif value == timedelta.min:
        result.scale = TimeSpanScale.MINMAX
        result.value = -1
    elif ticks % TicksPerMillisecond == 0:
        if ticks % TicksPerSecond == 0:
            if ticks % TicksPerMinute == 0:
                if ticks % TicksPerHour == 0:
                    if ticks % TicksPerDay == 0:
                        result.scale = TimeSpanScale.DAYS
                        result.value = int(ticks / TicksPerDay)
                    else:
                        result.scale = TimeSpanScale.HOURS
                        result.value = int(ticks / TicksPerHour)
                else:
                    result.scale = TimeSpanScale.MINUTES
                    result.value = int(ticks / TicksPerMinute)
            else:
                result.scale = TimeSpanScale.SECONDS
                result.value = int(ticks / TicksPerSecond)
        else:
            result.scale = TimeSpanScale.MILLISECONDS
            result.value = int(ticks / TicksPerMillisecond)
    else:
        result.scale = TimeSpanScale.TICKS
        result.value = ticks
    return result


def convertFromDateTimeToLocal(value):
    return toLocalTime(convertFromDateTime(value))


def getDateTimeNow():
    return convertToDateTime(datetime.now())


def buildTagValue(name, value=None):
    result = TagValue()
    result.name = name
    result.value = convertToVariant(value)
    return result


def buildSimpleTagList(list):
    return [buildTagValue(x) for x in list]


def buildWriteTagValue(name, value):
    result = TagValue()
    result.name = name
    result.tstamp = getDateTimeNow()
    result.value = convertToVariant(value)
    return result


def buildWriteTagListFromMap(tagmap):
    return [buildWriteTagValue(name, value) for name, value in list(tagmap.items())]


def buildTagDeclare(name):
    result = TagDeclare()
    result.name = name
    result.maxAge = 1000 * 60 * 3
    result.sampleRate = 3000
    return result


def buildSimpleTagDeclareList(list):
    return [buildTagDeclare(x) for x in list]


# convert a common.variant into proper object
def convertFromVariant(value):
    if value is None:
        return None

    try:
        #print((VariantType.UINT32, value.type, value.u4, repr(value.__dict__)))
        return {
            VariantType.EMPTY: None,
            VariantType.DOUBLE: value.r8,
            VariantType.FLOAT: value.r4,
            VariantType.FIXED32: value.f4,
            VariantType.FIXED64: value.f8,
            VariantType.INT32: value.i4,
            VariantType.INT64: value.i8v,
            VariantType.UINT32: value.u4,
            VariantType.UINT64: value.u8,
            VariantType.SINT32: value.si4,
            VariantType.SINT64: value.si8,
            VariantType.SFIXED32: value.sf4,
            VariantType.SFIXED64: value.sf8,
            VariantType.BOOL: value.b,
            VariantType.STRING: value.s,
            VariantType.BYTES: value.a,
            VariantType.OBJECT: value.a,
        }.get(getattr(value, 'type'), value)
    except Exception as ex:
        print(ex)
        pass
    return None


def convertToVariant(value):
    # import pdb; pdb.set_trace()
    v = variant()
    v.type = VariantType.EMPTY

    def assign(val, **kwargs):
        for k in kwargs:
            setattr(val, k, kwargs[k])
        return val

    t = type(value)
    try:
        v = {
            FloatType: lambda v: assign(v, type=VariantType.DOUBLE, r8=value),
            IntType: lambda v: assign(v, type=VariantType.INT32, i4=value),
            LongType: lambda v: assign(v, type=VariantType.INT64, i8v=value),
            StringType: lambda v: assign(v, type=VariantType.STRING, s=value),
            UnicodeType: lambda v: assign(v, type=VariantType.STRING, s=str(value)),
            BooleanType: lambda v: assign(v, type=VariantType.BOOL, b=value),
        }.get(type(value), lambda v: v)(v)
    except:
        pass
    return v


# Processor which stores state information on thread 
class ThreadContextProcessor(Thrift.TProcessor):
  """Wrapper class for processor to expose underlying transport"""
  __tls = threading.local()

  def __init__(self, proc):
    self.__proc = proc
    
  def process(self, iprot, oprot):
    try:
      # save iprot and prot on tls for later retrieval
      ThreadContextProcessor.__tls.iprot = iprot
      ThreadContextProcessor.__tls.oprot = oprot
      self.__proc.process(iprot, oprot)			
    finally:
      # reset tls variables
      ThreadContextProcessor.__tls.iprot = None
      ThreadContextProcessor.__tls.oprot = None
      
  def getInputProcessor():
    return ThreadContextProcessor.__tls.iprot
    
  def getOutputProcessor():
    return ThreadContextProcessor.__tls.iprot

# Framed transport which exposes underlying transport
class FramedTransport(TTransport.TFramedTransport, TTransport.CReadableTransport):

  class Factory:
    """Factory transport that builds buffered transports"""
    def getTransport(self, trans):
      buffered = TagFramedTransport(trans)
      return buffered

  def __init__(self, trans,):
    TTransport.TFramedTransport.__init__(self, trans)
    
  def getUnderlyingTransport(self):
    return self.__trans
    
# Framed transport which exposes underlying transport
class ZipFramedTransport(TTransport.TTransportBase, TTransport.CReadableTransport):
  """Class that wraps another transport and frames its I/O when writing."""

  class Factory:
    """Factory transport that builds buffered transports"""
    def getTransport(self, trans):
      buffered = ZipFramedTransport(trans)
      return buffered
    
  def __init__(self, trans,):
    self.__trans = trans
    self.__rbuf = StringIO()
    self.__wbuf = StringIO()

  def getUnderlyingTransport(self):
    return self.__trans
    
  def isOpen(self):
    return self.__trans.isOpen()

  def open(self):
    return self.__trans.open()

  def close(self):
    return self.__trans.close()

  def read(self, sz):
    ret = self.__rbuf.read(sz)
    if len(ret) != 0:
      return ret

    self.readFrame()
    return self.__rbuf.read(sz)

  def readFrame(self):
    buff = self.__trans.readAll(4)
    sz, = unpack('!i', buff)
    self.__rbuf = StringIO(zlib.decompress(self.__trans.readAll(sz)))

  def write(self, buf):
    self.__wbuf.write(buf)

  def flush(self):
    wout = zlib.compress(str(self.__wbuf.getvalue()))
    wsz = len(wout)
    # reset wbuf before write/flush to preserve state on underlying failure
    self.__wbuf = StringIO()
    # N.B.: Doing this string concatenation is WAY cheaper than making
    # two separate calls to the underlying socket object. Socket writes in
    # Python turn out to be REALLY expensive, but it seems to do a pretty
    # good job of managing string buffer operations without excessive copies
    buf = pack("!i", wsz) + wout
    self.__trans.write(buf)
    self.__trans.flush()

  # Implement the CReadableTransport interface.
  @property
  def cstringio_buf(self):
    return self.__rbuf

  def cstringio_refill(self, prefix, reqlen):
    # self.__rbuf will already be empty here because fastbinary doesn't
    # ask for a refill until the previous buffer is empty.  Therefore,
    # we can start reading new frames immediately.
    while len(prefix) < reqlen:
      self.readFrame()
      prefix += self.__rbuf.getvalue()
    self.__rbuf = StringIO(prefix)
    return self.__rbuf
    
    
# convert a common.variant into proper object
def getTypeNameFromVariant(value):
    return VariantType._VALUES_TO_NAMES.get(getattr(value, 'type'), 'EMPTY')


def getTagStatusString(value):
    return TagStatus._VALUES_TO_NAMES.get(value, 'E_TAG_BAD')


# override for variant data type
def __variant_repr_override__(self):
    return '%s(%s: %r)' % ( self.__class__.__name__, getTypeNameFromVariant(self), convertFromVariant(self) )


# generic thrift replacement for thrift classes only showing non-default values
def __thrift_repr_override__(self):
    L = ['%s=%r' % (x[2], getattr(self, x[2])) for x in self.__class__.thrift_spec if
         x is not None and getattr(self, x[2]) != x[4]]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))


def __DateTime_repr_override__(self):
    return "%s('%s')" % (self.__class__.__name__, convertFromDateTimeToLocal(self))


def __TimeSpan_repr_override__(self):
    return "%s('%s')" % (self.__class__.__name__, convertFromTimeSpan(self))

# override class representations with more readable forms
ReadTagResponse.__repr__ = __thrift_repr_override__
TagValue.__repr__ = __thrift_repr_override__
DateTime.__repr__ = __DateTime_repr_override__
TimeSpan.__repr__ = __TimeSpan_repr_override__
variant.__repr__ = __variant_repr_override__
