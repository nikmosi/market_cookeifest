const extractId = (input) => {
    if (/^\d+$/.test(input)) {
      return input;
    }
  
    try {
      const pathname = new URL(input).pathname;
      return pathname.split('/')[2];
    } catch (error) {
      console.error("Некорректный ввод", error);
      return null;
    }
  };

export default extractId
  