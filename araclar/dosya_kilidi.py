"""Hook durumunun oku-degistir-yaz islemini surecler arasinda korur."""
import os
import time
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def kilit(yol: Path, bekleme: float = 3.0):
    yol.parent.mkdir(parents=True, exist_ok=True)
    with yol.open('a+b') as f:
        if f.seek(0, 2) == 0:
            f.write(b'0')
            f.flush()
        bitis = time.monotonic() + bekleme
        while True:
            try:
                f.seek(0)
                if os.name == 'nt':
                    import msvcrt
                    msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() >= bitis:
                    raise TimeoutError('hook durum kilidi alinamadi')
                time.sleep(0.02)
        try:
            yield
        finally:
            f.seek(0)
            if os.name == 'nt':
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
