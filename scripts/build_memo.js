const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, AlignmentType, PageOrientation
} = require('docx');

const US_LETTER = { width: 12240, height: 15840 };

function labelValueRow(label, value) {
  return new TableRow({
    children: [
      new TableCell({
        width: { size: 2200, type: WidthType.DXA },
        children: [new Paragraph({ children: [new TextRun({ text: label, bold: true, font: 'Arial', size: 20 })] })],
        margins: { top: 80, bottom: 80, left: 100, right: 100 },
      }),
      new TableCell({
        width: { size: 7000, type: WidthType.DXA },
        children: [new Paragraph({ children: [new TextRun({ text: value, font: 'Arial', size: 20 })] })],
        margins: { top: 80, bottom: 80, left: 100, right: 100 },
      }),
    ],
  });
}

const headerTable = new Table({
  width: { size: 9200, type: WidthType.DXA },
  columnWidths: [2200, 7000],
  borders: {
    top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
    left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
    insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE },
  },
  rows: [
    labelValueRow('To:', 'Rajesh Malhotra, Chief Operating Officer'),
    labelValueRow('From:', 'Data Analytics Team'),
    labelValueRow('Date:', 'August 21, 2026'),
    labelValueRow('Re:', 'Board Prep — Region, Momentum & the Marketplace Channel Question'),
  ],
});

function sectionHeading(text) {
  return new Paragraph({
    spacing: { before: 300, after: 120 },
    children: [new TextRun({ text, bold: true, font: 'Arial', size: 24, color: '1F4E78' })],
  });
}

function bodyPara(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 160 },
    children: [new TextRun({ text, font: 'Arial', size: 22, ...opts })],
  });
}

function bullet(text) {
  return new Paragraph({
    bullet: { level: 0 },
    spacing: { after: 100 },
    children: [new TextRun({ text, font: 'Arial', size: 22 })],
  });
}

function statTableRow(cells, opts = {}) {
  return new TableRow({
    children: cells.map((text, i) => new TableCell({
      width: { size: opts.widths ? opts.widths[i] : 2300, type: WidthType.DXA },
      shading: opts.header ? { type: ShadingType.CLEAR, fill: '1F4E78' } : undefined,
      children: [new Paragraph({
        alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.CENTER,
        children: [new TextRun({
          text, font: 'Arial', size: 20,
          bold: !!opts.header, color: opts.header ? 'FFFFFF' : '000000',
        })],
      })],
      margins: { top: 80, bottom: 80, left: 100, right: 100 },
    })),
  });
}

const q1Table = new Table({
  width: { size: 9200, type: WidthType.DXA },
  columnWidths: [4600, 4600],
  rows: [
    statTableRow(['Metric', 'Value'], { header: true, widths: [4600, 4600] }),
    statTableRow(['Top region', 'South'], { widths: [4600, 4600] }),
    statTableRow(['South total revenue', '₹1,06,05,827'], { widths: [4600, 4600] }),
    statTableRow(['North (2nd place)', '₹90,46,262 (~15% behind)'], { widths: [4600, 4600] }),
  ],
});

const q2Table = new Table({
  width: { size: 9200, type: WidthType.DXA },
  columnWidths: [3067, 3067, 3066],
  rows: [
    statTableRow(['Transition', 'MoM % Change', 'Direction'], { header: true, widths: [3067, 3067, 3066] }),
    statTableRow(['April → May', '+7.8%', ''], { widths: [3067, 3067, 3066] }),
    statTableRow(['May → June', '+4.5%', ''], { widths: [3067, 3067, 3066] }),
    statTableRow(['Overall (Jan–Jun)', '+42.2% cumulative', 'Growing'], { widths: [3067, 3067, 3066] }),
  ],
});

const q3Table = new Table({
  width: { size: 9200, type: WidthType.DXA },
  columnWidths: [2300, 2300, 2300, 2300],
  rows: [
    statTableRow(['Channel', 'Revenue Share', 'Avg Order Value', 'Jan→Jun Growth'], { header: true, widths: [2300, 2300, 2300, 2300] }),
    statTableRow(['App', '41.0%', '₹6,938', '+31.2%'], { widths: [2300, 2300, 2300, 2300] }),
    statTableRow(['Website', '32.9%', '₹7,900', '+0.9%'], { widths: [2300, 2300, 2300, 2300] }),
    statTableRow(['Marketplace', '26.0%', '₹10,366', '+158.2%'], { widths: [2300, 2300, 2300, 2300] }),
  ],
});

const doc = new Document({
  sections: [{
    properties: {
      page: { size: US_LETTER, margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } },
    },
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 60 },
        children: [new TextRun({ text: 'UrbanKart', bold: true, font: 'Arial', size: 32, color: '1F4E78' })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 260 },
        children: [new TextRun({ text: 'Board Meeting Prep — Revenue & Channel Memo', font: 'Arial', size: 22, italics: true, color: '666666' })],
      }),
      headerTable,
      new Paragraph({ spacing: { after: 120 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'CCCCCC' } }, children: [] }),

      sectionHeading('Q1 — Which region is carrying us?'),
      bodyPara('South is the top-performing region, generating ₹1,06,05,827 in total revenue over Jan–Jun 2026 — the leadership instinct is correct. North is close behind at ₹90,46,262, only about 15% lower, so South\u2019s lead is real but not overwhelming.'),
      q1Table,

      sectionHeading('Q2 — Revenue momentum'),
      bodyPara('Revenue grew every month from January to June. The two most recent transitions:'),
      q2Table,
      bodyPara('Growth is positive in both recent months, though the pace is decelerating slightly (7.8% \u2192 4.5%) — worth watching, but the trend is unambiguously up.', { italics: true, size: 20 }),

      sectionHeading('Q3 — The channel decision'),
      bodyPara('Part A: Marketplace has the lowest total revenue of the three channels, holding 26.0% of total revenue (App: 41.0%, Website: 32.9%).'),
      q3Table,

      new Paragraph({
        spacing: { before: 240, after: 120 },
        children: [new TextRun({ text: 'Part B — Memo to Rajesh Malhotra', bold: true, font: 'Arial', size: 22, color: '1F4E78' })],
      }),
      bodyPara('Recommendation: Do not pause Marketplace.', { bold: true }),
      bodyPara('Total revenue makes Marketplace look weakest, but two other metrics say the opposite. First, trajectory: Marketplace revenue grew 158% from January to June \u2014 by far our fastest-growing channel \u2014 while Website grew just 0.9% over the same period and actually declined 14.9% month-on-month in the May-to-June transition. Second, order economics: Marketplace carries the highest average order value at ₹10,366 per order, versus ₹7,900 for Website and ₹6,938 for App \u2014 it is converting fewer orders, but each one is worth more.'),
      bodyPara('Marketplace is behind on volume because it is newer momentum, not dead weight. If the goal is cutting cost from underperformance, Website is the channel that actually warrants scrutiny \u2014 it is larger today but losing steam.'),
      bodyPara('Next step: Hold Marketplace as-is, and dig into what drove Website\u2019s May\u2192June dip before Q3 budget decisions are finalized.'),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync('UrbanKart_COO_Memo.docx', buf);
  console.log('saved');
});
