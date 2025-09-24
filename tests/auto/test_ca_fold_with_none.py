# Copyright 2023-2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pythonic_fp.circulararray.auto import CA, ca


def lt20(n: int | None, m: int | None) -> int | None:
    if n is None or m is None:
        return None
    if (sum := n + m) < 20:
        return sum
    return None


class TestFoldingWithNone:
    def test_foldl(self) -> None:
        """Edge cases"""
        c0: CA[int | None] = ca()

        try:
            c0.foldl(lt20)
        except ValueError:
            assert True
        else:
            assert False
        assert c0.foldl(lt20, 0) == 0
        assert c0.foldl(lt20, 42) == 42

        c1_5: CA[int | None] = ca(5)
        c1_42: CA[int | None] = ca(42)
        c1_none: CA[int | None] = ca(None)

        assert c1_5.foldl(lt20) == 5
        assert c1_42.foldl(lt20) == 42
        assert c1_none.foldl(lt20) is None

        assert c1_5.foldl(lt20, 4) == 9
        assert c1_42.foldl(lt20, 0) == None
        assert c1_none.foldl(lt20, 5) is None

        c4: CA[int | None] = ca(1, 2, 3, 4)
        c5_none = ca(1, 1, None, 1, 1)
        c7: CA[int | None] = ca(1, 2, 3, 4, 5, 6, 7)

        assert c4.foldl(lt20) == 10
        assert c4.foldl(lt20, -1) == 9
        assert c5_none.foldl(lt20) is None
        assert c5_none.foldl(lt20, 1) is None
        assert c7.foldl(lt20) is None 
        assert c7.foldl(lt20, -10) is 18 

      
