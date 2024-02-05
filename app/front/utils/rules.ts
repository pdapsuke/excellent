export const useRules = () => {
  return ValidationRules
}

class ValidationRules {
  // 必須入力のバリデーション
  public static required(v: string) {
    return !!v || "Required."
  }

  // 文字列長の最大値のバリデーション
  public static maxLength(n: number) {
    return (v: string) => {
      return (v && v.length <= n) || `Must be less than ${n} characters.`
    }
  }

  // 文字列長の最小値のバリデーション
  public static minLength(n: number) {
    return (v: string) => {
      return (v && v.length >= n) || `Must be more than ${n} characters.`
    }
  }

  // 数値の最大値のバリデーション
  public static max(n: number) {
    return (v: string | number) => {
      const num = typeof v === "string" ? parseInt(v) : v
      return (!isNaN(num) && num <= n) || `Must be less than ${n}.`
    }
  }

  // 数値の最小値のバリデーション
  public static min(n: number) {
    return (v: string | number) => {
      const num = typeof v === "string" ? parseInt(v) : v
      return (!isNaN(num) && num >= n) || `Must be more than ${n}.`
    }
  }

  // パスワードポリシーのバリデーション
  // 8文字以上, 少なくとも 1 つの数字を含む, 少なくとも 1 つの特殊文字を含む, 少なくとも 1 つの大文字を含む, 少なくとも 1 つの小文字を含む
  public static passwordValidate(v: string) {
    const passwordRegex = /^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[=+\-_.!@#$%^&*(),<>|:{};\/?`~"]).{8,}$/gi
    return (v && passwordRegex.test(v)) || "More than 8 characters, At least one digit, uppercase, lowercase letter, special character(^ $ * . [ ] { } ( ) ? - \" ! @ # % & / \\ , > < ' : ; | _ ~ ` + =)"
  }

  // Eメールアドレス形式のバリデーション
  public static emailValidate(v: string) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return (v && emailRegex.test(v) || "Must be email address format")
  }

  // 入力したEmailアドレスと確認用のものが一致するか
  public static emailConfirm(v: string) {
    return (confirm: string) => {
      return (v == confirm) || "The addresses you entered do not match."
    }
  }
}
