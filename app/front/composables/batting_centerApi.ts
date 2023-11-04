// ユーザー作成時のリクエストボディの型定義
interface UserPost {
    username: string
    password: string
    age: number
    role_ids: number[]
  }

// useBattingCenterApiの名前で関数をエクスポート
export const useBattingCenterApi = () => {
    return {
      // 都道府県/市区町村ごとのバッティングセンター一覧取得
      async post(prefecture_city: string) {
        return useApi().post<any>("getBattingCenters", "/batting_centers/", {"prefecture_city": prefecture_city})
      },
    }
  }
  