import { createTheme } from "@mui/material/styles"
import { PaletteMode } from "@mui/material"

const baseColors = {
  generalBackground: "#FADADD",
  cardBackground: "#FBE8D3",
  titleColor: "#4B3B30",
  secondaryText: "#C39A6B",
  primaryButton: {
    background: "#91B8C8",
    text: "#FFFFFF",
    hover: "#7BA1B0",
  },
  secondaryButton: {
    background: "#F7A6B2",
    text: "#4B3B30",
    hover: "#EC8C9F",
  },
  textField: {
    background: "#F8F4EB",
    border: "#C39A6B",
    text: "#4B3B30",
    placeholder: "#C39A6B",
  },
}

export const buildCustomTheme = (mode: PaletteMode) =>
  createTheme({
    palette: {
      mode,
      background: {
        default: baseColors.generalBackground,
        paper: baseColors.cardBackground,
      },
      primary: {
        main: baseColors.primaryButton.background,
        contrastText: baseColors.primaryButton.text,
      },
      secondary: {
        main: baseColors.secondaryButton.background,
        contrastText: baseColors.secondaryButton.text,
      },
      text: {
        primary: baseColors.titleColor,
        secondary: baseColors.secondaryText,
      },
    },
    typography: {
      fontFamily: `'Quicksand', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif`,
      allVariants: {
        color: baseColors.titleColor,
      },
    },
    components: {
      MuiPaper: {
        styleOverrides: {
          root: {
            borderRadius: "8px",
            backgroundColor: baseColors.cardBackground,
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: "8px",
            textTransform: "none",
            fontWeight: 600,
          },
          containedPrimary: {
            backgroundColor: baseColors.primaryButton.background,
            color: baseColors.primaryButton.text,
            "&:hover": {
              backgroundColor: baseColors.primaryButton.hover,
            },
          },
          containedSecondary: {
            backgroundColor: baseColors.secondaryButton.background,
            color: baseColors.secondaryButton.text,
            "&:hover": {
              backgroundColor: baseColors.secondaryButton.hover,
            },
          },
        },
      },
      MuiTextField: {
        styleOverrides: {
          root: {
            backgroundColor: baseColors.textField.background,
            "& .MuiOutlinedInput-root": {
              "& fieldset": {
                borderColor: baseColors.textField.border,
              },
              "&:hover fieldset": {
                borderColor: baseColors.secondaryText,
              },
            },
            "& input::placeholder": {
              color: baseColors.textField.placeholder,
            },
          },
        },
      },
    },
  })
