// ユーザー作成時のリクエストボディの型定義
interface UserPost {
  jwt_token: string
}

// ユーザー更新時のリクエストボディの型定義
interface UserPut {
    username: string
    password: string
    age: number
    role_ids: number[]
}

// ユーザー取得時のレスポンスボディの型定義
interface UserResponse {
  id: number
  username: string
  age: string
}

// ユーザー(行った！)更新時のリクエストボディの型定義
interface UserIttaPut {
  username: string
  place_id: string
  itta: string
}

interface AttaNakattaUpdate {
  username: string
  machine_id: number
  atta_nakatta: string
  add_atta_nakatta: string
}


// useUserApiの名前で関数をエクスポート
export const useUserApi = () => {
  return {
    // ユーザー一覧取得
    async getAll() {
      return useApi().get<UserResponse>("getUsers", "/users/")
    },
    // 指定したIDのユーザー取得
    async get(id: number) {
      return useApi().get<UserResponse>("getUser", `/users/${id}`)
    },
    // ユーザーサインイン
    async signIn(token: string) {
      return useApi().post<UserResponse>("signInUser", "/users/signin", {}, {"Authorization": `Bearer ${token}`})
    },
    // ユーザー更新
    async update(id: number, user: UserPut) {
      return useApi().put<UserResponse>("updateUser", `/users/${id}`, user)
    },
    // ユーザー削除
    async delete(id: number) {
        return useApi().delete<any>("deleteUser", `/users/${id}`)
    },
    // 行った！バッティングセンターを更新
    async updateItta(user: UserIttaPut) {
      return useApi().put<any>("putUserItta", "/users/me/itta", user)
    },
    // マシン情報のあった！なかった！を更新
    async updateAttaNakatta(input: AttaNakattaUpdate) {
      return useApi().put<any>("updateAttaNakatta", "/users/me/atta_nakatta", input)
    },
  }
}