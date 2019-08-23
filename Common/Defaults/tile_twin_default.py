from typing import List
from core.enums.caverna_enums import TileTypeEnum

class TileTwinDefault(object):

    def assign(self, currentTiles: List[TileTypeEnum]) -> List[TileTypeEnum]:
        if currentTiles is None:
            raise ValueError()

        currentTiles.clear()
        currentTiles.extend( [
            TileTypeEnum.meadowFieldTwin,
            TileTypeEnum.cavernTunnelTwin,
            TileTypeEnum.cavernCavernTwin,
            TileTypeEnum.pastureTwin,
            TileTypeEnum.oreMineDeepTunnelTwin ] )
        return currentTiles