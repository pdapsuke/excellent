// アイテム作成時のリクエストボディの型定義
interface ItemPost {
  title: string
  content: string
}

// アイテム更新時のリクエストボディの型定義
interface ItemPut {
  id: number
  title: string
  content: string
}

// アイテム取得時のレスポンスボディの型定義
interface ItemResponse {
  id: number
  title: string
  content: string
}

// usePrefectureCityApiの名前で関数をエクスポート
export const usePrefectureCityApi = () => {
  return {
    // 都道府県一覧取得
    async getAllPrefecture() {
      return useApi().get<any>("getPrefecture", "/prefecture/")
    },
    // 都道府県一覧取得
    async getCity(id: string) {
      return useApi().get<any>("getCity", `/city/${id}`)
    },
  }
}
