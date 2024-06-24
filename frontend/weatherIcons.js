export const getWeatherIcon = (condition) => {
  if (!condition) return "🌤️"; // Default icon if condition is undefined
  switch (condition.toLowerCase()) {
    case "clear":
      return "🌞";
    case "sunny":
      return "🌞";
    case "rain":
      return "🌧️";
    case "clouds":
      return "☁️";
    case "snowy":
      return "❄️";
    default:
      return "🌤️";
  }
};
