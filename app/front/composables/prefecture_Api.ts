interface Prefecture {
  prefCode: number
  prefName: string
}

interface City {
  prefCode: number
  cityCode: string
  cityName: string
  bigCityFlag: string
}

// usePrefectureCityApiの名前で関数をエクスポート
export const usePrefectureCityApi = () => {
  return {
    // 都道府県一覧取得
    async getAllPrefecture() {
      return useApi().get<Prefecture>("getPrefecture", "/prefecture/")
    },
    // 市区町村一覧取得
    async getCity(id: string) {
      return useApi().get<City>("getCity", `/city/${id}`)
    },
  }
}
