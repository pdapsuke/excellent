interface BattingCenter {
  id: number
  place_id: string
  name: string
  formatted_address: string
  photos: any[] | undefined
  itta_count: number
  itta: string
}

interface IttaResponse {
  id: number
  itta_count: number
  itta: string
}

// useBattingCenterApiの名前で関数をエクスポート
export const useBattingCenterApi = () => {
    return {
      // 都道府県/市区町村ごとのバッティングセンター一覧取得
      async searchBattingCenters(prefecture_city: string) {
        return useApi().get<BattingCenter>("searchBattingCenters", "/batting_centers/", {"prefecture_city": prefecture_city})
      },
      // バッティングセンターの詳細情報を取得
      async getDetail(username: string, place_id: string) {
        return useApi().get<any>("getDetail", `/batting_centers/${place_id}`, {"username": username})
      },
      // バッティングセンターに行った！したユーザーの追加
      async addIttaUser(battingcenterId: number) {
        return useApi().post<IttaResponse>("addIttaUser", `/batting_centers/${battingcenterId}`)
      },
      // バッティングセンターに行った！したユーザーの削除
      async removeIttaUser(battingcenterId: number) {
        return useApi().delete<IttaResponse>("removeIttaUser", `/batting_centers/${battingcenterId}`)
      },
    }
  }
  