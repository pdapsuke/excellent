export const useRules = () => {
  return ValidationRules
}

class ValidationRules {
  // 必須入力のバリデーション
  public static required(v: string) {
    return !!v || "入力必須です。"
  }

  // 1つ以上の配列要素バリデーション
  public static arrayElementRequired(v: number[]) {
    return (!!v && v.length >= 1) || "入力必須です。"
  }

  // パスワードポリシーのバリデーション
  // 8文字以上, 少なくとも 1 つの数字を含む, 少なくとも 1 つの特殊文字を含む, 少なくとも 1 つの大文字を含む, 少なくとも 1 つの小文字を含む
  public static passwordValidate(v: string) {
    const passwordRegex = /^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[=+\-_.!@#$%^&*(),<>|:{};\/?`~"]).{8,}$/gi
    return (v && passwordRegex.test(v)) || "8文字以上, 少なくとも一つの数字, 大文字・小文字アルファベット, 次の特殊文字(^ $ * . [ ] { } ( ) ? - \" ! @ # % & / \\ , > < ' : ; | _ ~ ` + =)を含めてください。"
  }

  // ユーザネームのバリデーション
  // 使える文字は、a～z, A～Z, 0～9, および特殊文字 (+ = , . @ -)
  public static userNameValidate(v: string) {
    const userNameRegex = /^(?=.*[a-zA-Z0-9+,\.@-]).{1,}$/
    return (v && userNameRegex.test(v)) || "使える文字は、a～z, A～Z, 0～9, および特殊文字 (+ = , . @ -) です。"
  }

  // Eメールアドレス形式のバリデーション
  public static emailValidate(v: string) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return (v && emailRegex.test(v) || "Eメール形式である必要があります。")
  }

  // 入力したEmailアドレスと確認用のものが一致するか
  public static emailConfirm(v: string) {
    return (confirm: string) => {
      return (v == confirm) || "入力したアドレスが一致しません。"
    }
  }
}
