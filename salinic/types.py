from typing import Optional

from typing_extensions import Annotated

from .field import IdField, KeywordField, NumericField, TextField

IdPrimary = Annotated[int, IdField(primary_key=True)]

IdStrPrimary = Annotated[str, IdField(primary_key=True)]
IdStr = Annotated[Optional[str], IdField()]
OptionalStrId = Annotated[Optional[str], IdField()]

Text = Annotated[str, TextField()]
OptionalText = Annotated[Optional[str], TextField()]

OptionalNumeric = Annotated[Optional[int], NumericField()]

Keyword = Annotated[str, KeywordField()]
OptionalKeyword = Annotated[Optional[list[str]], KeywordField()]
