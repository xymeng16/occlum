use super::*;

#[derive(Debug)]
pub struct DevZero;

impl File for DevZero {
    fn read(&self, _buf: &mut [u8]) -> Result<usize> {
        for b in _buf.iter_mut() {
            *b = 0;
        }
        Ok(_buf.len())
    }

    fn read_at(&self, _offset: usize, _buf: &mut [u8]) -> Result<usize> {
        self.read(_buf)
    }

    fn readv(&self, bufs: &mut [&mut [u8]]) -> Result<usize> {
        let mut total_nbytes = 0;
        for buf in bufs {
            total_nbytes += self.read(buf)?;
        }
        Ok(total_nbytes)
    }

    fn write(&self, _buf: &[u8]) -> Result<usize> {
        return_errno!(EINVAL, "device not support writes")
    }

    fn write_at(&self, _offset: usize, _buf: &[u8]) -> Result<usize> {
        return_errno!(EINVAL, "device not support writes")
    }

    fn writev(&self, bufs: &[&[u8]]) -> Result<usize> {
        return_errno!(EINVAL, "device not support writes")
    }

    fn seek(&self, pos: SeekFrom) -> Result<off_t> {
        return_errno!(EINVAL, "device not support seeks")
    }

    fn metadata(&self) -> Result<Metadata> {
        unimplemented!()
    }

    fn set_len(&self, len: u64) -> Result<()> {
        return_errno!(EINVAL, "device not support resizing")
    }

    fn sync_all(&self) -> Result<()> {
        Ok(())
    }

    fn sync_data(&self) -> Result<()> {
        Ok(())
    }

    fn read_entry(&self) -> Result<String> {
        return_errno!(ENOTDIR, "device is not a directory")
    }

    fn as_any(&self) -> &Any {
        self
    }
}